from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import ClusterModel, EntityModel, UserModel


class Neo4J_CreateClustersHelper(INeo4JQueryHelper):
    """
    Creates a new clusters

    params:
        clusters: list[ClusterModel] (cluster_id is ignored and will be overwritten)

    returns:
        {
            'clusters': list[ClusterModel]
        }
    """

    def __init__(self, clusters: list[ClusterModel]):
        super().__init__(
            name='create_clusters',
            query=Query('''
                UNWIND $props AS prop
                CREATE (c:Cluster {
                    cluster_id: apoc.create.uuid(),
                    cluster_name: prop.cluster_name,
                    cluster_vector: prop.cluster_vector
                })
                RETURN c
            ''')
        )
        self.clusters = clusters

    def get_arguments(self) -> dict:
        return {
            'props': [
                {
                    'cluster_name': cluster.cluster_name,
                    'cluster_vector': cluster.cluster_vector
                }
                for cluster in self.clusters
            ]
        }

    def consume(self, result: list[Record]) -> dict:
        return {'clusters': [ClusterModel.from_dict_separate_entities(record['c'], []) for record in result]}
