from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import EntityModel


class Neo4J_DeleteAllEntitiesHelper(INeo4JQueryHelper):
    """
    Deletes all entities in the database.

    params:
        None

    returns:
        {
            'entities': list[EntityModel]
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
        return {'entities': [EntityModel.from_dict(record['e']) for record in result]}
