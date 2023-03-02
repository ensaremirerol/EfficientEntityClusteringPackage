from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_DeleteClusterHelper(INeo4JQueryHelper):
    """
    Deletes a cluster
    Returns None if the cluster does not exist

    params:
        cluster_id: str

    returns:
        {
            'cluster': Neo4JCluster | None
        }

    """

    def __init__(self, cluster_id: str):
        super().__init__(
            name='delete_cluster',
            query=Query('''
                MATCH (c:Cluster {cluster_id: $cluster_id})
                DETACH DELETE c
                RETURN c
            ''')
        )
        self.cluster_id = cluster_id

    def get_arguments(self) -> dict:
        return {
            'cluster_id': self.cluster_id
        }

    def consume(self, result: list[Record]) -> dict:
        if len(result) != 1:
            return {'cluster': None}
        entities: list[Neo4JEntity] = [record['e'] for record in result] if result[0]['e'] else []
        return {'cluster': Neo4JCluster.from_dict(result[0]['c'], entities=entities)}
