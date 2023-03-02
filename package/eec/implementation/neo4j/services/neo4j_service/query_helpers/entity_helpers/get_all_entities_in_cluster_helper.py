from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import EntityModel


class Neo4J_GetAllEntitiesInClusterHelper(INeo4JQueryHelper):
    """
    Gets all entities which are in the cluster.

    params:
        None

    returns:
        {
            'entities': list[EntityModel] | None
        }
    """

    def __init__(self):
        super().__init__(
            'get_all_entities_in_cluster',
            query=Query('''
            MATCH (e:Entity)
            MATCH ()-[:HAS_ENTITY]->(e)
            RETURN e
            ''')
        )

    def consume(self, result: list[Record]) -> dict:
        return {
            'entities': [EntityModel.from_dict(record['e']) for record in result] if len(result) > 0 else []
        }
