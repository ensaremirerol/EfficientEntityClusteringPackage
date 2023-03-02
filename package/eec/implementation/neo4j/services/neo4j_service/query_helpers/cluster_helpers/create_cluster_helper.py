from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import ClusterModel, EntityModel, UserModel


class Neo4J_CreateClusterHelper(INeo4JQueryHelper):
    """
    Creates a new cluster

    params:
        cluster: ClusterModel (cluster_id is ignored and will be overwritten)

    returns:
        {
            'cluster': ClusterModel
        }
    """

    def __init__(self, cluster: ClusterModel):
        super().__init__(
            name='create_cluster',
            query=Query('''
                CREATE (c:Cluster {
                    cluster_id: apoc.create.uuid(),
                    cluster_name: $cluster_name,
                    cluster_vector: $cluster_vector
                }) RETURN c
            ''')
        )
        self.cluster = cluster

    def get_arguments(self) -> dict:
        return {'cluster_name': self.cluster.cluster_name, 'cluster_vector': self.cluster.cluster_vector}

    def consume(self, result: list[Record]) -> dict:
        return {'cluster': ClusterModel.from_dict_separate_entities(result[0]['c'], [])}
