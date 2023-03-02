from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity

from typing import cast


class Neo4J_GetAllClustersHelper(INeo4JQueryHelper):
    """
    Gets all clusters

    params:
        None

    returns:
        {
            'clusters': list[Neo4JCluster]
        }
    """

    def __init__(self):
        super().__init__(
            name='get_all_clusters',
            query=Query('''
                MATCH (c:Cluster)
                OPTIONAL MATCH (c)-[:HAS_ENTITY]->(e:Entity)
                RETURN c, COLLECT(e) AS e
            ''')
        )

    def consume(self, result: list[Record]) -> dict:
        return {
            'clusters': [
                Neo4JCluster.from_dict(record['c'],
                                       entities=[Neo4JEntity.from_dict(entity)
                                                 for entity in record['e']] if record['e'] else [])
                for record in result
            ]
        }
