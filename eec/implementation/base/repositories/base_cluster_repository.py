from core.data_model import *
from core.exceptions import *
from core.abstract.cluster_repository import IClusterRepository
from implementation.base.repositories import BaseEntityRepository

import numpy as np
from typing import Optional, Callable, cast


class BaseClusterRepository(IClusterRepository):
    def __init__(
            self, entity_repository: BaseEntityRepository, clusters: list[ClusterModel] = [],
            last_cluster_id: int = 0):
        self.entity_repository = entity_repository
        self.clusters: list[ClusterModel] = clusters
        self.last_cluster_id = last_cluster_id

    def get_cluster_by_id(self, cluster_id: str) -> ClusterModel:
        '''Returns the cluster with the given cluster id.'''
        for cluster in self.clusters:
            if cluster.cluster_id == cluster_id:
                return cluster
        raise NotFoundException('Cluster with id {cluster_id} not found.')

    def get_all_clusters(self) -> list[ClusterModel]:
        return [cluster for cluster in self.clusters]

    def add_cluster(self, cluster: ClusterModel) -> ClusterModel:
        '''Adds the given cluster to the repository.'''
        for o in self.clusters:
            if o.cluster_name == cluster.cluster_name:
                raise AlreadyExistsException(
                    f'Cluster with name {cluster.cluster_name} already exists.\n Duplicate cluster names are not allowed')
        cluster.cluster_id = str(self.last_cluster_id)
        self.last_cluster_id += 1

        self.clusters.append(cluster)

        return cluster

    def add_clusters(self, clusters: list[ClusterModel]) -> list[ClusterModel]:
        '''Adds the given clusters to the repository.'''
        return [self.add_cluster(cluster) for cluster in clusters]

    def update_cluster(self, cluster: ClusterModel) -> ClusterModel:
        '''Updates the given cluster in the repository.'''
        for o in self.clusters:
            if o.cluster_id == cluster.cluster_id:
                cluster.cluster_name = cluster.cluster_name
                return cluster
        raise NotFoundException('Cluster with id {cluster_id} not found.')

    def delete_cluster(self, cluster_id: str) -> ClusterModel:
        for i in range(len(self.clusters)):
            if self.clusters[i].cluster_id == cluster_id:
                for entity in self.clusters[i].entities:
                    entity.cluster_id = None
                    entity.has_cluster = False
                return self.clusters.pop(i)
        raise NotFoundException('Cluster with id {cluster_id} not found.')

    def delete_clusters(self, cluster_ids: list[str]) -> list[ClusterModel]:
        return [self.delete_cluster(cluster_id) for cluster_id in cluster_ids]

    def delete_all_clusters(self):
        self.clusters = []

    def remove_entity_from_cluster(self, entity_id: str) -> EntityModel:
        entity = self.entity_repository.get_entity_by_id(entity_id)
        if entity.cluster_id is None or entity.cluster_id == '' or not entity.has_cluster:
            raise NotFoundException('Entity with id {entity_id} not found in any cluster.')
        cluster = self.get_cluster_by_id(entity.cluster_id)
        cluster.entities.remove(entity)
        entity.cluster_id = None
        entity.has_cluster = False
        cluster.cluster_vector = np.mean(
            [entity.mention_vector for entity in cluster.entities],
            axis=0).tolist()
        return entity

    def remove_entities_from_cluster(
            self, entity_ids: list[str]) -> list[EntityModel]:
        return [self.remove_entity_from_cluster(entity_id) for entity_id in entity_ids]

    def add_entity_to_cluster(self, cluster_id: str, entity_id: str):
        cluster = self.get_cluster_by_id(cluster_id)
        entity = self.entity_repository.get_entity_by_id(entity_id)
        cluster.entities.append(entity)
        entity.cluster_id = cluster.cluster_id
        entity.has_cluster = True
        cluster.cluster_vector = np.mean(
            [entity.mention_vector for entity in cluster.entities],
            axis=0).tolist()

    def to_dict(self) -> dict:
        return {
            'clusters': [cluster.to_dict() for cluster in self.clusters],
            'last_cluster_id': self.last_cluster_id
        }

    @classmethod
    def from_dict(cls, cluster_repository_dict: dict, entity_repository: BaseEntityRepository) -> 'BaseClusterRepository':
        return cls(
            entity_repository,
            [ClusterModel.from_dict(cluster_dict)
             for cluster_dict in cluster_repository_dict['clusters']],
            cluster_repository_dict['last_cluster_id'])

    def encode(self) -> dict:
        return {
            'clusters': [
                {
                    'cluster_id': cluster.cluster_id,
                    'cluster_name': cluster.cluster_name,
                    'entities': [entity.entity_id for entity in cluster.entities],
                    'cluster_vector': cluster.cluster_vector
                } for cluster in self.clusters
            ],
            'last_cluster_id': self.last_cluster_id
        }

    @classmethod
    def decode(cls, cluster_repository_dict: dict, entity_repository: BaseEntityRepository) -> 'BaseClusterRepository':
        return cls(
            entity_repository,
            [
                ClusterModel(
                    cluster_id=cluster_dict['cluster_id'],
                    cluster_name=cluster_dict['cluster_name'],
                    entities=[entity_repository.get_entity_by_id(entity_id)
                              for entity_id in cluster_dict['entities']],
                    cluster_vector=cluster_dict['cluster_vector'])
                for cluster_dict in cluster_repository_dict['clusters']],
            cluster_repository_dict['last_cluster_id'])
