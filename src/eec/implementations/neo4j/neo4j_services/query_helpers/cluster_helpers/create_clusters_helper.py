from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_CreateClustersHelper(INeo4JQueryHelper):
    """
    Creates a new clusters

    params:
        clusters: list[Neo4JCluster] (cluster_id is ignored and will be overwritten)

    returns:
        {
            'clusters': list[Neo4JCluster]
        }
    """

    def __init__(self, clusters: list[Neo4JCluster]):
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
                    'cluster_vector': cluster.cluster_vector.tolist()
                }
                for cluster in self.clusters
            ]
        }

    def consume(self, result: list[Record]) -> dict:
        return {'clusters': [Neo4JCluster.from_dict(record['c'], []) for record in result]}
