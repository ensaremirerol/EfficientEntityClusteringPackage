from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_GetAllEntitiesInClusterHelper(INeo4JQueryHelper):
    """
    Gets all entities which are in the cluster.

    params:
        None

    returns:
        {
            'entities': list[Neo4JEntity] | None
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
            'entities': [Neo4JEntity.from_dict(record['e']) for record in result] if len(result) > 0 else None
        }
