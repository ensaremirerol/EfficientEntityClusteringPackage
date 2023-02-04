from src.implementations.base.models.base_entity import BaseEntity
from src.implementations.base.repositories.base_entity_repository import BaseEntityRepository
from src.implementations.base.models.base_cluster import BaseCluster
from src.interfaces.interface_cluster_repository.i_cluster_repository import IClusterRepository
from src.exceptions.general.exceptions import *

import numpy as np
from typing import Optional, Callable


class BaseClusterRepository(IClusterRepository):
    def __init__(self, entity_repository: BaseEntityRepository, last_cluster_id: int):
        self.entity_repository = entity_repository
        self.clusters: list[BaseCluster] = []
        self.last_cluster_id = last_cluster_id

    def get_cluster_by_id(self, cluster_id: str) -> BaseCluster:
        '''Returns the cluster with the given cluster id.'''
        for cluster in self.clusters:
            if cluster.cluster_id == cluster_id:
                return cluster
        raise NotFoundException('Cluster with id {cluster_id} not found.')

    def get_all_clusters(self) -> list[BaseCluster]:
        return [cluster for cluster in self.clusters]

    def add_cluster(self, cluster: BaseCluster):
        '''Adds the given cluster to the repository.'''
        cluster.cluster_id = str(self.last_cluster_id)
        self.last_cluster_id += 1

        self.clusters.append(cluster)

    def add_clusters(self, clusters: list[BaseCluster]):
        '''Adds the given clusters to the repository.'''
        for cluster in clusters:
            self.add_cluster(cluster)

    def delete_cluster(self, cluster_id: str):
        for cluster in self.clusters:
            if cluster.cluster_id == cluster_id:
                self.clusters.remove(cluster)
                return
        raise NotFoundException('Cluster with id {cluster_id} not found.')

    def delete_clusters(self, cluster_ids: list[str]):
        for cluster in self.clusters:
            if cluster.cluster_id in cluster_ids:
                self.clusters.remove(cluster)
                continue
            print(f'Cluster with id {cluster.cluster_id} not found. Skipping...')

    def delete_all_clusters(self):
        self.clusters = []

    def remove_entity_from_cluster(self, cluster_id: Optional[str], entity_id: str) -> BaseEntity:
        entity = None
        if cluster_id is not None:
            cluster = self.get_cluster_by_id(cluster_id)
            entity = cluster.remove_entity(entity_id)
            return entity
        for cluster in self.clusters:
            if cluster.is_in_cluster(entity_id=entity_id):
                entity = cluster.remove_entity(entity_id)

        if entity is not None:
            return entity

        raise NotFoundException('Entity with id {entity_id} not found in cluster/s.')

    def remove_entities_from_cluster(
            self, cluster_id: Optional[str],
            entity_ids: list[str]) -> list[BaseEntity]:
        return [self.remove_entity_from_cluster(cluster_id, entity_id) for entity_id in entity_ids]
