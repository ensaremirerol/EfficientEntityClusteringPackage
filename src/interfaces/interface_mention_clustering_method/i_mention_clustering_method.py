from src.interfaces.interface_cluster.i_cluster import ICluster
from src.interfaces.interface_cluster_repository.i_cluster_repository import IClusterRepository
from src.interfaces.interface_entity.i_entity import IEntity
from src.interfaces.interface_entity_repository.i_entity_repository import IEntityRepository

import abc
from typing import Optional, Callable


class IMentionClusteringMethod(abc.ABC):
    def __init__(self, name: str, cluster_repository: IClusterRepository,
                 entity_repository: IEntityRepository):
        self.name: str = name
        self.cluster_repository = cluster_repository
        self.entity_repository = entity_repository

    @abc.abstractmethod
    def getPossibleClusters(self, entity: IEntity) -> list[ICluster]:
        '''Returns a list of possible clusters for the given entity.'''
        pass
