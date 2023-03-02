from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_GetAllEntitiesHelper(INeo4JQueryHelper):
    """
    Gets all entities in the database.

    params:
        None

    returns:
        {
            'entities': list[Neo4JEntity] | None
        }
    """

    def __init__(self, ):
        super().__init__('get_all_entities', query=Query(
            '''
            MATCH (e:Entity)
            OPTIONAL MATCH (c:Cluster)-[:HAS_ENTITY]->(e)
            SET e.cluster_id = COALESCE(c.cluster_id, null)
            SET e.in_cluster = COALESCE(c.cluster_id IS NOT NULL, false)
            RETURN e
            '''))

    def consume(self, result: list[Record]) -> dict:
        return {
            'entities': [Neo4JEntity.from_dict(record['e']) for record in result] if len(result) > 0 else []
        }
