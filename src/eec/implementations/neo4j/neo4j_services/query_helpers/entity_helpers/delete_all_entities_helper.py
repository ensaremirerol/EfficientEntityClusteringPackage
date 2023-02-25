from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_DeleteAllEntitiesHelper(INeo4JQueryHelper):
    """
    Deletes all entities in the database.

    params:
        None

    returns:
        {
            'entities': list[Neo4JEntity]
        }
    """

    def __init__(self,):
        super().__init__('delete_all_entities', query=Query(
            '''
                MATCH (e:Entity)
                DELETE e
                RETURN e
            '''
        ))

    def consume(self, result: list[Record]) -> dict:
        return {'entities': [Neo4JEntity.from_dict(record['e']) for record in result]}
