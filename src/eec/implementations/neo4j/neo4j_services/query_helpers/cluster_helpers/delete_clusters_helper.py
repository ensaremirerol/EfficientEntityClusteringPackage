from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_DeleteClustersHelper(INeo4JQueryHelper):
    """
    Deletes clusters

    params:
        cluster_ids: list[str]

    returns:
        {
            'clusters': list[Neo4JCluster]
        }

    """

    def __init__(self, cluster_ids: list[str]):
        super().__init__(
            name='delete_clusters',
            query=Query('''
                UNWIND $cluster_ids AS cluster_id
                MATCH (c:Cluster {cluster_id: $cluster_id})
                DETACH DELETE c
                RETURN c
            ''')
        )
        self.cluster_ids = cluster_ids

    def get_arguments(self) -> dict:
        return {
            'cluster_ids': self.cluster_ids
        }

    def consume(self, result: list[Record]) -> dict:
        if len(result) == 0:
            return {'clusters': None}
        return {
            'clusters': [
                Neo4JCluster.from_dict(record['c'], entities=[])
                for record in result
            ]
        }
