from src.eec.implementations.base import *


class EntityClustererBridge:
    '''
        This class just gathers the required objects for the process.
        It does not contain any logic.
    '''

    def __init__(self, entity_repository: BaseEntityRepository,
                 cluster_repository: BaseClusterRepository,
                 mention_clustering_method: BaseMentionClusteringMethod):
        self.entity_repository = entity_repository
        self.cluster_repository = cluster_repository
        self.mention_clustering_method = mention_clustering_method

    