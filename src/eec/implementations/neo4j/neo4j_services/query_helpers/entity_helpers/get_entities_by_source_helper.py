from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_GetEntitiesBySourceHelper(INeo4JQueryHelper):
    """
    Gets all entities which have the given source.
    Returns None if no entities are found.

    params:
        entity_source: str

    returns:
        {
            'entities': list[Neo4JEntity] | None
        }
    """

    def __init__(self, entity_source: str):
        super().__init__(
            'get_entity_by_source',
            query=Query('''MATCH (e:Entity {entity_source: $source}) RETURN e''')
        )
        self.entity_source = entity_source

    def get_arguments(self) -> dict:
        return {'entity_source': self.entity_source}

    def consume(self, result: list[Record]) -> dict:
        return {
            'entities': [Neo4JEntity.from_dict(record['e']) for record in result] if len(result) > 0 else []
        }
