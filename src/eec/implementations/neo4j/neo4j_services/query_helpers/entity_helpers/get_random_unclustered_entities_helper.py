from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_GetRandomUnclusteredEntitiesHelper(INeo4JQueryHelper):
    """
    Gets a random unclustered entities.
    Returns None if there are no unclustered entities.

    params:
        n: int

    returns:
        {
            'entities': list[Neo4JEntity] | None
        }

    """

    def __init__(self, n: int):
        super().__init__('get_random_unclustered_entities', query=Query(
            '''
                MATCH (e:Entity) WITH e, rand() AS r 
                WHERE NOT ()-[:HAS_ENTITY]->(e)
                RETURN e ORDER BY r LIMIT $n
            '''
        ))
        self.n = n

    def get_arguments(self) -> dict:
        return {
            'n': self.n
        }

    def consume(self, result: list[Record]) -> dict:
        return {'entities': [Neo4JEntity.from_dict(record['e']) for record in result] if len(result) > 0 else []}
