from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_CreateEntityHelper(INeo4JQueryHelper):
    """
    Creates an entity in the database.
    
    params:
        entity: Neo4JEntity

    returns:
        {
            'entity': Neo4JEntity
        }

    """
    def __init__(self, entity: Neo4JEntity):
        super().__init__('create_entity', query=Query(
            '''
                CREATE (e:Entity {
                    entity_id: apoc.create.uuid(),
                    mention: $mention,
                    entity_source: $entity_source,
                    entity_source_id: $entity_source_id,
                    has_mention_vector: $has_mention_vector,
                    mention_vector: $mention_vector
                }) RETURN e
            '''
        ))
        self.entity = entity

    def get_arguments(self) -> dict:
        return {
            'mention': self.entity.mention,
            'entity_source': self.entity.entity_source,
            'entity_source_id': self.entity.entity_source_id,
            'has_mention_vector': self.entity.has_mention_vector,
            'mention_vector': self.entity.mention_vector.tolist()
        }

    def consume(self, result: list[Record]) -> dict:
        return {'entity': Neo4JEntity.from_dict(result[0]['e'])}
