from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import EntityModel


class Neo4J_GetAllEntitiesHelper(INeo4JQueryHelper):
    """
    Gets all entities in the database.

    params:
        None

    returns:
        {
            'entities': list[EntityModel] | None
        }
    """

    def __init__(self, ):
        super().__init__('get_all_entities', query=Query(
            '''
            MATCH (e:Entity)
            OPTIONAL MATCH (c:Cluster)-[:HAS_ENTITY]->(e)
            SET e.cluster_id = COALESCE(c.cluster_id, null)
            SET e.has_cluster = COALESCE(c.cluster_id IS NOT NULL, false)
            RETURN e
            '''))

    def consume(self, result: list[Record]) -> dict:
        return {
            'entities': [EntityModel.from_dict(record['e']) for record in result] if len(result) > 0 else []
        }
