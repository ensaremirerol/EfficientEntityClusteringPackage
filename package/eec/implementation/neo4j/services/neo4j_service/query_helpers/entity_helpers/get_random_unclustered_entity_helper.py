from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import EntityModel


class Neo4J_GetRandomUnclusteredEntityHelper(INeo4JQueryHelper):
    """
    Gets a random unclustered entity.
    Returns None if there are no unclustered entities.

    params:
        None

    returns:
        {
            'entity': EntityModel | None
        }

    """

    def __init__(self,):
        super().__init__('get_random_unclustered_entity', query=Query(
            '''
                MATCH (e:Entity) WITH e, rand() AS r 
                WHERE NOT ()-[:HAS_ENTITY]->(e)
                RETURN e ORDER BY r LIMIT 1
            '''
        ))

    def consume(self, result: list[Record]) -> dict:
        return {'entity': EntityModel.from_dict(result[0]['e']) if len(result) == 1 else None}
