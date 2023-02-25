from eec.interfaces.interface_mention_clustering_method.i_mention_clustering_method import IMentionClusteringMethod
from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity
from eec.implementations.neo4j.repositories.neo4j_cluster_repository import Neo4JClusterRepository
from eec.implementations.neo4j.repositories.neo4j_entity_repository import Neo4JEntityRepository
from eec.implementations.neo4j.neo4j_services.neo4j_helper import Neo4JHelper
from eec.implementations.neo4j.neo4j_services.query_helpers.method_helpers import *

from eec.exceptions.general.exceptions import *

import numpy as np
import gensim
from typing import Optional, cast
from difflib import SequenceMatcher

import logging

class Neo4JMentionClusteringMethod(IMentionClusteringMethod):
    def __init__(self, name: str, cluster_repository: Neo4JClusterRepository,
                 entity_repository: Neo4JEntityRepository, top_n: int = 10, alpha: float = 0.5, beta: float = 0.3, gamma: float = 0.2):
        self.name: str = name
        self.cluster_repository = cluster_repository
        self.entity_repository = entity_repository
        self.top_n = top_n
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.logger = logging.getLogger(__name__)
        self.neo4j_helper = Neo4JHelper.get_instance()


    def getPossibleClusters(self, entity: Neo4JEntity) -> list[Neo4JCluster]:

        def vector_similarity(vectors: np.ndarray, target: np.ndarray) -> np.ndarray:
            similarities = np.dot(vectors, target) / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(target))
            return similarities

        def ws_sim(string: str, target: str) -> float:
            return SequenceMatcher(None, string, target).ratio()
        
        def ps_sim(string: str, target: str) -> float:
            return np.mean([SequenceMatcher(None, target, word).ratio() for word in string.split(" ")]).astype(float)

        if not entity.has_mention_vector:
            self.logger.warning("No mention vector found Fallback to only string similarity")
            return self._fallback_get_possible_clusters(entity)
        
        result = self.neo4j_helper.run_query(
            Neo4J_GetClosestClustersHelper(
                self.top_n,
            entity.get_mention_vector().tolist())
        )

        top_clusters : list[Neo4JCluster] = result['clusters']
        vector_similarities = np.array(result['similarities'])

        cluster_entities = []
        for cluster in top_clusters:
            cluster_entities.append(cluster.get_closest_entities(entity, distance_function=vector_similarity, top_n=10))
        
        cluster_entity_ws_sim = []
        cluster_entity_ps_sim = []
        for o_entities in cluster_entities:
            _ws_sim = [ws_sim(o_entity.get_mention(), entity.get_mention()) for o_entity in o_entities]
            _ps_sim = [ps_sim(o_entity.get_mention(), entity.get_mention()) for o_entity in o_entities]
        
            _whole_string_similaritiy = np.mean(_ws_sim)
            _partial_string_similaritiy = np.mean(_ps_sim)
            cluster_entity_ws_sim.append(_whole_string_similaritiy)
            cluster_entity_ps_sim.append(_partial_string_similaritiy)

        cluster_entity_ws_sim = np.array(cluster_entity_ws_sim)
        cluster_entity_ps_sim = np.array(cluster_entity_ps_sim)

        cluster_entity_ws_sim_index = []
        other_clusters = []

        for i in range(len(cluster_entity_ws_sim)):
            if cluster_entity_ws_sim[i] > self.gamma:
                cluster_entity_ws_sim_index.append(i)
            else:
                other_clusters.append(i)


        # whole string cluster sort
        ws_cluster_sorted = np.argpartition(cluster_entity_ws_sim, -len(cluster_entity_ws_sim_index))[-len(cluster_entity_ws_sim_index):]

        # other cluster scores
        other_cluster_scores = np.multiply(vector_similarities[other_clusters], self.alpha) + np.multiply(cluster_entity_ps_sim[other_clusters], self.beta)
        other_cluster_scores_sorted = np.argpartition(other_cluster_scores, -len(other_cluster_scores))[-len(other_cluster_scores):]

        return [top_clusters[index] for index in ws_cluster_sorted] + [top_clusters[index] for index in other_cluster_scores_sorted]

    def _fallback_get_possible_clusters(self, entity: Neo4JEntity) -> list[Neo4JCluster]:
        def ws_sim(string: str, target: str) -> float:
            return SequenceMatcher(None, string, target).ratio()

        mention = entity.get_mention()
        all_entities_in_cluster: list[Neo4JEntity] = self.entity_repository.get_all_entities_in_cluster()

        if len(all_entities_in_cluster) == 0:
            self.logger.warning("Fallback failed! Create new cluster!")
            return []

        _top_n = min(self.top_n, len(all_entities_in_cluster))
        
        ws_sim_scores = [ws_sim(o_entity.get_mention(), mention) for o_entity in all_entities_in_cluster]
        top_entity_indexes = np.argpartition(ws_sim_scores, -_top_n)[-_top_n:]
        top_entities = [all_entities_in_cluster[index] for index in top_entity_indexes]
        top_entities_ids = [o_entity.get_id() for o_entity in top_entities]
        top_clusters : list[Neo4JCluster] = self.cluster_repository.cluster_of_entities(top_entities_ids)
        return top_clusters
        

            