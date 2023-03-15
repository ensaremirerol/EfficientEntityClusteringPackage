from eec.core.abstract.mention_clustering_method import IMentionClusteringMethod
from eec.core.data_model import ClusterModel, EntityModel
from eec.implementation.neo4j.repositories.neo4j_cluster_repository import Neo4JClusterRepository
from eec.implementation.neo4j.repositories.neo4j_entity_repository import Neo4JEntityRepository
from eec.implementation.neo4j.services.neo4j_service.neo4j_helper import Neo4JHelper
from eec.implementation.neo4j.services.neo4j_service.query_helpers.method_helpers import *


import numpy as np
from difflib import SequenceMatcher
from typing import Callable, cast

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


    def getPossibleClusters(self, entity: EntityModel) -> list[ClusterModel]:
        """
            Tries to find the most similar clusters to the given entity

            How it works:
                1. Get the top n clusters with the highest cosine similarity to the entity mention vector
                2. Get the top n entities from each cluster
                3. Calculate the whole string similarity ratio for each entity in each cluster and average the ratios
                4. Sort the clusters by the average string similarity ratio and return the top n clusters

            params:
                entity: EntityModel
            returns:
                list[ClusterModel]
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
            entity.mention_vector)
        )

        # Set the new top n to the number of clusters found
        _top_n = min(self.top_n, len(result['clusters']))

        top_clusters : list[ClusterModel] = result['clusters']

        cluster_entities = []
        for cluster in top_clusters:
            cluster_entities.append(self._get_closest_entities(cluster, entity, distance_function=vector_similarity, top_n=10))

        cluster_entity_ws_sim = [] # whole string similarity ratios

        # Calculate the string similarity ratios for each entity in each cluster. Average the ratios for each cluster
        for o_entities in cluster_entities:
            _ws_sim = [ws_sim(o_entity.mention, entity.mention) for o_entity in o_entities]
        
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
    

    def _get_closest_entities(self, cluster: ClusterModel, entity: EntityModel, distance_function: Callable, top_n) -> list[EntityModel]:
        top_n = min(top_n, len(cluster.entities))
        _all_entity_vectors = np.array([entity.mention_vector for entity in cluster.entities])
        similarities = distance_function(_all_entity_vectors, np.array(entity.mention_vector))
        return [cluster.entities[i] for i in np.argpartition(similarities, -top_n)[-top_n:]]

    def _fallback_get_possible_clusters(self, entity: EntityModel) -> list[ClusterModel]:
        """
            Tries to find the most similar clusters to the given entity by searching all entities that are in cluster
        """
        def ws_sim(string: str, target: str) -> float:
            return SequenceMatcher(None, string, target).ratio()

        # Get the mention of the entity
        mention = entity.mention

        # Get the all other entities that are in clusters
        all_entities_in_cluster: list[EntityModel] = self.entity_repository.get_all_entities_in_cluster()

        if len(all_entities_in_cluster) == 0:
            self.logger.warning("Fallback failed! Create new cluster!")
            return []

        _top_n = min(self.top_n, len(all_entities_in_cluster))
        
        ws_sim_scores = [ws_sim(o_entity.mention, mention) for o_entity in all_entities_in_cluster]
        top_entity_indexes = np.argpartition(ws_sim_scores, -_top_n)[-_top_n:]
        top_entities: list[EntityModel] = [all_entities_in_cluster[index] for index in top_entity_indexes]
        top_entities_ids = [o_entity.entity_id for o_entity in top_entities]
        top_clusters : list[ClusterModel] = self.cluster_repository.cluster_of_entities(top_entities_ids)
        
        # remove duplicates

        result = []
        for cluster in top_clusters:
            if cluster not in result:
                result.append(cluster)
        
        return result
        

            