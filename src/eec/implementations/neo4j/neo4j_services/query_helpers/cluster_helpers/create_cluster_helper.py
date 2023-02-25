from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_CreateClusterHelper(INeo4JQueryHelper):
    """
    Creates a new cluster

    params:
        cluster: Neo4JCluster (cluster_id is ignored and will be overwritten)
        
    returns:
        {
            'cluster': Neo4JCluster
        }
    """

    def __init__(self, cluster: Neo4JCluster):
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
        return {'cluster_name': self.cluster.cluster_name, 'cluster_vector': self.cluster.cluster_vector.tolist()}

    def consume(self, result: list[Record]) -> dict:
        return {'cluster': Neo4JCluster.from_dict(result[0]['c'], [])}
