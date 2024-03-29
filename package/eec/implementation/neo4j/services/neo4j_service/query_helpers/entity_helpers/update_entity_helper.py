from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import EntityModel


class Neo4J_UpdateEntityHelper(INeo4JQueryHelper):
    """
    Updates an entity in the database.
    Returns None if no entity by that id exists.

    params:
        entity: EntityModel

    returns:
        {
            'entity': EntityModel | None
        }

    """

    def __init__(self, entity: EntityModel):
        super().__init__('update_entity', query=Query(
            '''
                MATCH (e:Entity {entity_id: $entity_id})
                SET e.mention = $mention,
                    e.entity_source = $entity_source,
                    e.entity_source_id = $entity_source_id,
                    e.has_cluster = $in_cluster,
                    e.cluster_id = $cluster_id,
                    e.has_mention_vector = $has_mention_vector,
                    e.mention_vector = $mention_vector
                RETURN e
            '''
        ))
        self.entity = entity

    def get_arguments(self) -> dict:
        return {
            'entity_id': self.entity.entity_id,
            'mention': self.entity.mention,
            'entity_source': self.entity.entity_source,
            'entity_source_id': self.entity.entity_source_id,
            'in_cluster': self.entity.has_cluster,
            'cluster_id': self.entity.cluster_id,
            'has_mention_vector': self.entity.has_mention_vector,
            'mention_vector': self.entity.mention_vector
        }

    def consume(self, result: list[Record]) -> dict:
        return {'entity': EntityModel.from_dict(result[0]['e']) if len(result) == 1 else None}
