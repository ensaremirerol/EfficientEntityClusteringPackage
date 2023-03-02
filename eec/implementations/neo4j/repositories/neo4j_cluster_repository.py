from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity
from eec.implementations.neo4j.repositories.neo4j_entity_repository import Neo4JEntityRepository
from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.interfaces.interface_cluster_repository.i_cluster_repository import IClusterRepository
from eec.exceptions.general.exceptions import *
from eec.implementations.neo4j.neo4j_services.neo4j_helper import Neo4JHelper
from eec.implementations.neo4j.neo4j_services.query_helpers.cluster_helpers import *

import numpy as np
from typing import Optional, Callable, cast

from neo4j import Driver


class Neo4JClusterRepository(IClusterRepository):
    def __init__(
            self, entity_repository: Neo4JEntityRepository):
        self.entity_repository = entity_repository
        self.neo4j_helper = Neo4JHelper.get_instance()

    def get_cluster_by_id(self, cluster_id: str) -> Neo4JCluster:
        '''Returns the cluster with the given cluster id.'''
        result = self.neo4j_helper.run_query(
            Neo4J_GetClusterByIdHelper(cluster_id=cluster_id))
        if result['cluster'] is None:
            raise NotFoundException(
                f'Cluster with id {cluster_id} not found')
        return cast(Neo4JCluster, result['cluster'])

    def get_all_clusters(self) -> list[Neo4JCluster]:
        '''Returns all clusters.'''
        result = self.neo4j_helper.run_query(Neo4J_GetAllClustersHelper())
        return cast(list[Neo4JCluster], result['clusters'])

    def add_cluster(self, cluster: Neo4JCluster) -> Neo4JCluster:
        '''Adds the given cluster to the repository.'''
        result = self.neo4j_helper.run_query(
            Neo4J_CreateClusterHelper(cluster=cluster))
        return cast(Neo4JCluster, result['cluster'])

    def add_clusters(self, clusters: list[Neo4JCluster]) -> list[Neo4JCluster]:
        '''Adds the given clusters to the repository.'''
        result = self.neo4j_helper.run_query(
            Neo4J_CreateClustersHelper(clusters=clusters))
        return cast(list[Neo4JCluster], result['clusters'])

    def update_cluster(self, cluster: Neo4JCluster) -> Neo4JCluster:
        '''Updates the given cluster in the repository.'''
        result = self.neo4j_helper.run_query(
            Neo4J_UpdateClusterHelper(cluster=cluster))
        if result['cluster'] is None:
            raise NotFoundException(
                f'Cluster with id {cluster.cluster_id} not found.')
        return cast(Neo4JCluster, result['cluster'])

    def delete_cluster(self, cluster_id: str) -> Neo4JCluster:
        '''Deletes the cluster with the given cluster id.'''
        result = self.neo4j_helper.run_query(
            Neo4J_DeleteClusterHelper(cluster_id=cluster_id))
        if result['cluster'] is None:
            raise NotFoundException(
                f'Cluster with id {cluster_id} not found.')
        return cast(Neo4JCluster, result['cluster'])

    def delete_clusters(self, cluster_ids: list[str]) -> list[Neo4JCluster]:
        '''Deletes the clusters with the given cluster ids.'''
        result = self.neo4j_helper.run_query(
            Neo4J_DeleteClustersHelper(cluster_ids=cluster_ids))
        return cast(list[Neo4JCluster], result['clusters'])

    def delete_all_clusters(self):
        '''Deletes all clusters.'''
        self.neo4j_helper.run_query(Neo4J_DeleteAllClustersHelper())

    def remove_entity_from_cluster(self, cluster_id: str, entity_id: str) -> Neo4JEntity:
        '''Removes the entity with the given entity id from the cluster with the given cluster id.'''
        result = self.neo4j_helper.run_query(
            Neo4J_DetachClusterFromEntityHelper(cluster_id=cluster_id, entity_id=entity_id))
        if result['entity'] is None:
            raise NotFoundException(
                f'Entity with id {entity_id} not found.')
        if result['cluster'] is None:
            raise NotFoundException(
                f'Cluster with id {cluster_id} not found.')
        self.calculate_cluster_vector(cluster_id=cluster_id)
        return cast(Neo4JEntity, result['entity'])

    def remove_entities_from_clusters(
            self, cluster_id: str,
            entity_ids: list[str]) -> list[Neo4JEntity]:
        '''Removes the entities with the given entity ids from the cluster with the given cluster id.'''
        result = self.neo4j_helper.run_query(
            Neo4J_DetachEntitiesHelper(cluster_id=cluster_id, entity_ids=entity_ids))
        self.calculate_cluster_vector(cluster_id=cluster_id)

        return cast(
            list[Neo4JEntity],
            [result['objects'][i]['entity'] for i in range(len(entity_ids))])

    def add_entity_to_cluster(self, cluster_id: str, entity_id: str):
        '''Adds the entity with the given entity id to the cluster with the given cluster id.'''
        self.neo4j_helper.run_query(
            Neo4J_ConnectClusterToEntityHelper(cluster_id=cluster_id, entity_id=entity_id))
        self.calculate_cluster_vector(cluster_id=cluster_id)

    def cluster_of_entities(self, entity_ids: list[str]) -> list[Neo4JCluster]:
        '''Returns the cluster of the entity with the given entity id.'''
        result = self.neo4j_helper.run_query(
            Neo4J_GetClusterOfEntitiesHelper(entity_ids=entity_ids))
        return cast(list[Neo4JCluster], result['clusters'])

    def calculate_cluster_vector(self, cluster_id: str):
        '''Calculates the vector of the cluster with the given cluster id.'''
        result = self.neo4j_helper.run_query(
            Neo4J_GetEntityVectorsHelper(cluster_id=cluster_id))
        if result['vectors'] is None:
            raise NotFoundException(
                f'Cluster with id {cluster_id} not found.')

        vectors = np.array(result['vectors'])
        cluster_vector = np.array([])
        if vectors.shape[0] == 0:
            cluster_vector = np.array([])
        else:
            cluster_vector = np.mean(vectors, axis=0)
        self.neo4j_helper.run_query(Neo4J_SetClusterVectorHelper(
            cluster_id=cluster_id, cluster_vector=cluster_vector.tolist()))

    def to_dict(self) -> dict:
        return {
            'clusters': [cluster.to_dict() for cluster in self.get_all_clusters()],
        }
