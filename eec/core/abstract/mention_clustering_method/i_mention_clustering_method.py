from core.abstract.cluster_repository import IClusterRepository
from core.abstract.entity_repository import IEntityRepository
from core.data_model import ClusterModel, EntityModel

from abc import ABC, abstractmethod


class IMentionClusteringMethod(ABC):
    """
    Interface for a mention clustering method.
    """

    def __init__(self, cluster_repository: IClusterRepository,
                 entity_repository: IEntityRepository):
        self.name: str = 'IMentionClusteringMethod'
        self.cluster_repository = cluster_repository
        self.entity_repository = entity_repository

    @abstractmethod
    def getPossibleClusters(self, entity: EntityModel) -> list[ClusterModel]:
        '''Returns a list of possible clusters for the given entity.'''
        pass
