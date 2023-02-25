from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_DeleteAllClustersHelper(INeo4JQueryHelper):
    """
    Deletes all clusters

    params:
        None

    returns:
        {
            'clusters': list[Neo4JCluster]
        }

    """

    def __init__(self):
        super().__init__(
            name='delete_all_clusters',
            query=Query('''
                MATCH (c:Cluster)
                DETACH DELETE c
                RETURN c
            ''')
        )

    def consume(self, result: list[Record]) -> dict:
        return {
            'clusters': [
                Neo4JCluster.from_dict(record['c'],
                                       entities=[])
                for record in result
            ]
        }
