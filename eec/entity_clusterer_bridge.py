from eec.interfaces.interface_cluster_repository.i_cluster_repository import IClusterRepository
from eec.interfaces.interface_mention_clustering_method.i_mention_clustering_method import IMentionClusteringMethod
from eec.interfaces.interface_entity_repository.i_entity_repository import IEntityRepository
from eec.interfaces.interface_user_repository.i_user_repository import IUserRepository


class EntityClustererBridge:
    '''
        This class just gathers the required objects for the process.
        It does not contain any logic.
    '''

    entity_repository: IEntityRepository
    cluster_repository: IClusterRepository
    mention_clustering_method: IMentionClusteringMethod
    user_repository: IUserRepository

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
    
    def set_user_repository(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    