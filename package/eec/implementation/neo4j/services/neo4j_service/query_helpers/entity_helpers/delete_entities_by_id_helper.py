from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import EntityModel


class Neo4J_DeleteEntitiesByIdHelper(INeo4JQueryHelper):
    """
    Deletes entities by id in the database.

    params:
        entity_ids: list[str]

    returns:
        {
            'entities': list[EntityModel]
        }

    """

    def __init__(self, entity_ids: list[str]):
        super().__init__('delete_entities_by_id', query=Query(
            '''
                MATCH (e:Entity)
                WHERE e.entity_id IN $entity_ids
                DELETE e
                RETURN e
            '''
        ))
        self.entity_ids = entity_ids

    def get_arguments(self) -> dict:
        return {
            'entity_ids': self.entity_ids
        }

    def consume(self, result: list[Record]) -> dict:
        return {'entities': [EntityModel.from_dict(record['e']) for record in result]}
