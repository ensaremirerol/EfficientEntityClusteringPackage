from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import ClusterModel, EntityModel, UserModel

from typing import cast


class Neo4J_GetAllClustersHelper(INeo4JQueryHelper):
    """
    Gets all clusters

    params:
        None

    returns:
        {
            'clusters': list[ClusterModel]
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
                ClusterModel.from_dict_separate_entities(record['c'],
                                                         entities=[EntityModel.from_dict(entity)
                                                                   for entity in record['e']] if record['e'] else [])
                for record in result
            ]
        }
