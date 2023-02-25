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
    """
        Tries to find the most similar clusters to the given entity
        params:
            name: Name of the method
            cluster_repository: Cluster repository to get all clusters from
            entity_repository: Entity repository to get all entities from
            top_n: Number of clusters to return
    """
    def __init__(self, name: str, cluster_repository: Neo4JClusterRepository,
                 entity_repository: Neo4JEntityRepository, top_n: int = 10):
        self.name: str = name
        self.cluster_repository = cluster_repository
        self.entity_repository = entity_repository
        self.top_n = top_n
        self.logger = logging.getLogger(__name__)
        self.neo4j_helper = Neo4JHelper.get_instance()


    def getPossibleClusters(self, entity: Neo4JEntity) -> list[Neo4JCluster]:
        """
            Tries to find the most similar clusters to the given entity

            How it works:
                1. Get the top n clusters with the highest cosine similarity to the entity mention vector
                2. Get the top n entities from each cluster
                3. Calculate the whole string similarity ratio for each entity in each cluster and average the ratios
                4. Sort the clusters by the average string similarity ratio and return the top n clusters

            params:
                entity: Neo4JEntity
            returns:
                list[Neo4JCluster]
        """

        # Implementation of Cosine Similarity
        def vector_similarity(vectors: np.ndarray, target: np.ndarray) -> np.ndarray:
            similarities = np.dot(vectors, target) / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(target))
            return similarities

        # Whole string similarity
        def ws_sim(string: str, target: str) -> float:
            return SequenceMatcher(None, string, target).ratio()

        # Entity has no mention vector to compare with. Fallback to only string similarity
        if not entity.has_mention_vector:
            self.logger.warning("No mention vector found Fallback to only string similarity")
            return self._fallback_get_possible_clusters(entity)
        
        # Get the top n clusters with the highest cosine similarity to the entity mention vector
        result = self.neo4j_helper.run_query(
            Neo4J_GetClosestClustersHelper(
                self.top_n,
            entity.get_mention_vector().tolist())
        )

        # Set the new top n to the number of clusters found
        _top_n = min(self.top_n, len(result['clusters']))

        top_clusters : list[Neo4JCluster] = result['clusters']

        cluster_entities = []
        for cluster in top_clusters:
            cluster_entities.append(cluster.get_closest_entities(entity, distance_function=vector_similarity, top_n=10))

        cluster_entity_ws_sim = [] # whole string similarity ratios

        # Calculate the string similarity ratios for each entity in each cluster. Average the ratios for each cluster
        for o_entities in cluster_entities:
            _ws_sim = [ws_sim(o_entity.get_mention(), entity.get_mention()) for o_entity in o_entities]
        
            _whole_string_similaritiy = np.mean(_ws_sim)
            cluster_entity_ws_sim.append(_whole_string_similaritiy)

        cluster_entity_ws_sim = np.array(cluster_entity_ws_sim)

        # Sort the clusters by the average string similarity ratio and return the top n clusters

        top_cluster_indexes = np.argpartition(cluster_entity_ws_sim, -_top_n)[-_top_n:]

        _result = [top_clusters[index] for index in top_cluster_indexes]

        # remove duplicates
        result = []
        for cluster in _result:
            if cluster not in result:
                result.append(cluster)
        
        return result

    def _fallback_get_possible_clusters(self, entity: Neo4JEntity) -> list[Neo4JCluster]:
        """
            Tries to find the most similar clusters to the given entity by searching all entities that are in cluster
        """
        def ws_sim(string: str, target: str) -> float:
            return SequenceMatcher(None, string, target).ratio()

        # Get the mention of the entity
        mention = entity.get_mention()

        # Get the all other entities that are in clusters
        all_entities_in_cluster: list[Neo4JEntity] = self.entity_repository.get_all_entities_in_cluster()

        if len(all_entities_in_cluster) == 0:
            self.logger.warning("Fallback failed! Create new cluster!")
            return []

        _top_n = min(self.top_n, len(all_entities_in_cluster))
        
        ws_sim_scores = [ws_sim(o_entity.get_mention(), mention) for o_entity in all_entities_in_cluster]
        top_entity_indexes = np.argpartition(ws_sim_scores, -_top_n)[-_top_n:]
        top_entities = [all_entities_in_cluster[index] for index in top_entity_indexes]
        top_entities_ids = [o_entity.get_entity_id() for o_entity in top_entities]
        top_clusters : list[Neo4JCluster] = self.cluster_repository.cluster_of_entities(top_entities_ids)
        
        # remove duplicates

        result = []
        for cluster in top_clusters:
            if cluster not in result:
                result.append(cluster)
        
        return result
        

            