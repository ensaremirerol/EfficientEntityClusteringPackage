from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_DeleteEntityByIdHelper(INeo4JQueryHelper):
    """
    Deletes an entity by id in the database.
    Returns None if no entity by that id exists.

    params:
        entity_id: str

    returns:
        {
            'entity': Neo4JEntity | None
        }

    """

    def __init__(self, entity_id: str):
        super().__init__('delete_entity_by_id', query=Query(
            '''
                MATCH (e:Entity {entity_id: $entity_id})
                DELETE e
                RETURN e
            '''
        ))
        self.entity_id = entity_id

    def get_arguments(self) -> dict:
        return {
            'entity_id': self.entity_id
        }

    def consume(self, result: list[Record]) -> dict:
        return {'entity': Neo4JEntity.from_dict(result[0]['e'])}
