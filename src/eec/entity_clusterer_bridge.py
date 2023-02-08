from eec.interfaces.interface_cluster_repository.i_cluster_repository import IClusterRepository
from eec.interfaces.interface_mention_clustering_method.i_mention_clustering_method import IMentionClusteringMethod
from eec.interfaces.interface_entity_repository.i_entity_repository import IEntityRepository


class EntityClustererBridge:
    '''
        This class just gathers the required objects for the process.
        It does not contain any logic.
    '''

    def __init__(self):
        self.entity_repository = None
        self.cluster_repository = None
        self.mention_clustering_method = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EntityClustererBridge, cls).__new__(cls)
        return cls.instance

    def set_entity_repository(self, entity_repository: IEntityRepository):
        self.entity_repository = entity_repository

    def set_cluster_repository(self, cluster_repository: IClusterRepository):
        self.cluster_repository = cluster_repository

    def set_mention_clustering_method(self, mention_clustering_method: IMentionClusteringMethod):
        self.mention_clustering_method = mention_clustering_method

    