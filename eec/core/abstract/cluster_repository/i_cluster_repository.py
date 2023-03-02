from core.data_model import ClusterModel, EntityModel
from core.abstract.entity_repository import IEntityRepository


from typing import Optional
from abc import ABC, abstractmethod


class IClusterRepository(ABC):
    """
    Interface for a cluster repository.
    """

    def __init__(self, entity_repository: IEntityRepository):
        self.entity_repository = entity_repository

    @abstractmethod
    def get_cluster_by_id(self, cluster_id: str) -> ClusterModel:
        '''Returns the cluster with the given cluster id.'''
        pass

    @abstractmethod
    def get_all_clusters(self) -> list[ClusterModel]:
        '''Returns all clusters.'''
        pass

    @abstractmethod
    def add_cluster(self, cluster: ClusterModel) -> ClusterModel:
        '''Adds the given cluster.'''
        pass

    @abstractmethod
    def add_clusters(self, clusters: list[ClusterModel]) -> list[ClusterModel]:
        '''Adds the given clusters.'''
        pass

    @abstractmethod
    def update_cluster(self, cluster: ClusterModel) -> ClusterModel:
        '''Updates the given cluster.'''
        pass

    @abstractmethod
    def delete_cluster(self, cluster_id: str) -> ClusterModel:
        '''Deletes the given cluster.'''
        pass

    @abstractmethod
    def delete_clusters(self, cluster_ids: list[str]) -> list[ClusterModel]:
        '''Deletes the given clusters.'''
        pass

    @abstractmethod
    def delete_all_clusters(self):
        '''Deletes all clusters.'''
        pass

    @abstractmethod
    def remove_entity_from_cluster(self, entity_id: str) -> EntityModel:
        '''Removes the entity with the given entity id from its cluster.'''
        pass

    @abstractmethod
    def remove_entities_from_cluster(
            self, entity_ids: list[str]) -> list[EntityModel]:
        '''Removes the entities with the given entity ids from their clusters.'''
        pass

    @abstractmethod
    def add_entity_to_cluster(self, cluster_id: str, entity_id: str):
        '''Adds the entity with the given entity id to the cluster with the given cluster id.'''
        pass
