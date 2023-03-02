from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import EntityModel


class Neo4J_UpdateEntitiesHelper(INeo4JQueryHelper):
    """
    Updates the entities in the database.

    params:
        entities: list[EntityModel]

    returns:
        {
            'entities': list[EntityModel]
        }

    """

    def __init__(self, entities: list[EntityModel]):
        super().__init__('update_entities', query=Query(
            '''
                UNWIND $props AS prop
                MATCH (e:Entity {entity_id: $entity_id})
                SET 
                    e.mention = prop.mention,
                    e.entity_source = prop.entity_source,
                    e.entity_source_id = prop.entity_source_id,
                    e.in_cluster = prop.in_cluster,
                    e.cluster_id = prop.cluster_id,
                    e.has_mention_vector = prop.has_mention_vector,
                    e.mention_vector = prop.mention_vector
                RETURN e
            '''
        ))
        self.entities = entities

    def get_arguments(self) -> dict:
        return {
            'props': [
                {
                    'entity_id': entity.entity_id,
                    'mention': entity.mention,
                    'entity_source': entity.entity_source,
                    'entity_source_id': entity.entity_source_id,
                    'in_cluster': entity.has_cluster,
                    'cluster_id': entity.cluster_id,
                    'has_mention_vector': entity.has_mention_vector,
                    'mention_vector': entity.mention_vector
                } for entity in self.entities
            ]
        }

    def consume(self, result: list[Record]) -> dict:
        return {'entities': [EntityModel.from_dict(record['e']) for record in result] if len(result) > 0 else []}
