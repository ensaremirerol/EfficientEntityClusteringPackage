from src.interfaces.interface_cluster.i_cluster import ICluster
from src.interfaces.interface_entity_repository.i_entity_repository import IEntityRepository
from src.interfaces.interface_entity.i_entity import IEntity


import abc
from typing import Optional


class IClusterRepository(abc.ABC):
    def __init__(self, entity_repository: IEntityRepository):
        self.entity_repository = entity_repository

    @abc.abstractmethod
    def get_cluster_by_id(self, cluster_id: str) -> ICluster:
        '''Returns the cluster with the given cluster id.'''
        pass

    @abc.abstractmethod
    def get_all_clusters(self) -> list[ICluster]:
        '''Returns all clusters.'''
        pass

    @abc.abstractmethod
    def add_cluster(self, cluster: ICluster):
        '''Adds the given cluster.'''
        pass

    @abc.abstractmethod
    def add_clusters(self, clusters: list[ICluster]):
        '''Adds the given clusters.'''
        pass

    @abc.abstractmethod
    def delete_cluster(self, cluster_id: str):
        '''Deletes the given cluster.'''
        pass

    @abc.abstractmethod
    def delete_clusters(self, cluster_ids: list[str]):
        '''Deletes the given clusters.'''
        pass

    @abc.abstractmethod
    def delete_all_clusters(self):
        '''Deletes all clusters.'''
        pass

    @abc.abstractmethod
    def remove_entity_from_cluster(self, cluster_id: Optional[str], entity_id: str) -> IEntity:
        '''Removes the entity with the given entity id from its cluster.'''
        pass

    @abc.abstractmethod
    def remove_entities_from_clusters(
            self, cluster_id: Optional[str],
            entity_ids: list[str]) -> list[IEntity]:
        '''Removes the entities with the given entity ids from their clusters.'''
        pass

    @abc.abstractmethod
    def add_entity_to_cluster(self, cluster_id: str, entity_id: str):
        '''Adds the entity with the given entity id to the cluster with the given cluster id.'''
        pass
