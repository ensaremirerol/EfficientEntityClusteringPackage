from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_SetClusterVectorHelper(INeo4JQueryHelper):
    """
    Sets the cluster vector for a cluster
    Returns None if the cluster does not exist

    params:
        cluster_id: str
        cluster_vector: list[float]

    returns:
        {
            'cluster': Neo4JCluster | None (without entities)
        }

    """

    def __init__(self, cluster_id: str, cluster_vector: list[float]):
        super().__init__(
            name='set_cluster_vector',
            query=Query('''
                MATCH (c:Cluster {cluster_id: $cluster_id})
                SET c.cluster_vector = $cluster_vector
                RETURN c
            ''')
        )
        self.cluster_id = cluster_id
        self.cluster_vector = cluster_vector

    def get_arguments(self) -> dict:
        return {'cluster_id': self.cluster_id, 'cluster_vector': self.cluster_vector}

    def consume(self, result: list[Record]) -> dict:
        if len(result) != 1:
            return {'cluster': None}
        return {'cluster': Neo4JCluster.from_dict(result[0]['c'], entities=[])}
