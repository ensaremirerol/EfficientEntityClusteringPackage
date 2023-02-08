from src.eec.interfaces.interface_mention_clustering_method.i_mention_clustering_method import IMentionClusteringMethod
from src.eec.implementations.base.models.base_cluster import BaseCluster
from src.eec.implementations.base.models.base_entity import BaseEntity
from src.eec.implementations.base.repositories.base_entity_repository import BaseEntityRepository
from src.eec.implementations.base.repositories.base_cluster_repository import BaseClusterRepository

from src.eec.exceptions.general.exceptions import *

import numpy as np
import gensim
from typing import Optional, cast
from difflib import SequenceMatcher

class BaseMentionClusteringMethod(IMentionClusteringMethod):
    def __init__(self, name: str, cluster_repository: BaseClusterRepository,
                 entity_repository: BaseEntityRepository, top_n: int = 10, alpha: float = 0.5, beta: float = 0.3, gamma: float = 0.2):
        self.name: str = name
        self.cluster_repository = cluster_repository
        self.entity_repository = entity_repository
        self.top_n = top_n
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma


    def getPossibleClusters(self, entity: BaseEntity) -> list[BaseCluster]:

        def vector_similarity(vectors: np.ndarray, target: np.ndarray) -> np.ndarray:
            similarities = np.dot(vectors, target) / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(target))
            return similarities

        def ws_sim(string: str, target: str) -> float:
            return SequenceMatcher(None, string, target).ratio()
        
        def ps_sim(string: str, target: str) -> float:
            return np.mean([SequenceMatcher(None, target, word).ratio() for word in string.split(" ")]).astype(float)

        mention_vector = entity.get_mention_vector()
        if mention_vector is None:
            print("No mention vector found Fallback to only string similarity")
            return self._fallback_get_possible_clusters(entity)
        all_clusters = self.cluster_repository.clusters
        _all_vectors = [cluster.cluster_vector for cluster in all_clusters if cluster.cluster_vector.size > 0]
        
        if len(_all_vectors) == 0:
            print("No cluster vectors found Fallback to only string similarity")
            return self._fallback_get_possible_clusters(entity)

        _top_n = min(self.top_n, len(_all_vectors))

        all_vectors = np.array(_all_vectors)
        vector_similarities = vector_similarity(all_vectors, mention_vector)

        top_cluster_indexes = np.argpartition(vector_similarities, -_top_n)[-_top_n:]
        top_clusters : list[BaseCluster] = [all_clusters[index] for index in top_cluster_indexes]

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

        cluster_entity_ws_sim_index = np.where(cluster_entity_ws_sim >= self.gamma)
        other_clusters = np.where(cluster_entity_ws_sim < self.gamma)

        # other cluster scores
        other_cluster_scores = np.multiply(vector_similarities[other_clusters], self.alpha) + np.multiply(cluster_entity_ps_sim[other_clusters], self.beta)

        # whole string cluster sort
        ws_cluster_sorted = np.argpartition(cluster_entity_ws_sim, -len(cluster_entity_ws_sim_index))[-len(cluster_entity_ws_sim_index):]

        return [top_clusters[index] for index in ws_cluster_sorted] + [top_clusters[index] for index in other_clusters[0][np.argpartition(other_cluster_scores, -len(other_cluster_scores))[-len(other_cluster_scores):]]]

    def _fallback_get_possible_clusters(self, entity: BaseEntity) -> list[BaseCluster]:
        def ws_sim(string: str, target: str) -> float:
            return SequenceMatcher(None, string, target).ratio()

        mention = entity.get_mention()
        all_entities_in_cluster: list[BaseEntity] = self.entity_repository.get_all_entities_in_cluster()

        if len(all_entities_in_cluster) == 0:
            print("Fallback failed! Create new cluster")
            return []

        _top_n = min(self.top_n, len(all_entities_in_cluster))
        
        ws_sim_scores = [ws_sim(o_entity.get_mention(), mention) for o_entity in all_entities_in_cluster]
        top_entity_indexes = np.argpartition(ws_sim_scores, -_top_n)[-_top_n:]
        top_entities = [all_entities_in_cluster[index] for index in top_entity_indexes]
        top_clusters : list[BaseCluster] = [self.cluster_repository.get_cluster_by_id(o_entity.get_cluster_id()) for o_entity in top_entities]
        return top_clusters
        

            