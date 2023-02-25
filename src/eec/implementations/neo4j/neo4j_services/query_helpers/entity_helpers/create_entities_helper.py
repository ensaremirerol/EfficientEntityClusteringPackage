from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_CreateEntitiesHelper(INeo4JQueryHelper):
    """
    Creates entities in the database.

    params:
        entities: list[Neo4JEntity] - The entities to create.

    returns:
        {
            'entities': list[Neo4JEntity]
        }

    """

    def __init__(self, entities: list[Neo4JEntity]):
        super().__init__('create_entities', query=Query(
            '''
                UNWIND $props AS prop
                CREATE (e:Entity {
                    entity_id: apoc.create.uuid(),
                    mention: prop.mention,
                    entity_source: prop.entity_source,
                    entity_source_id: prop.entity_source_id,
                    in_cluster: prop.in_cluster,
                    cluster_id: prop.cluster_id,
                    has_mention_vector: prop.has_mention_vector,
                    mention_vector: prop.mention_vector
                }) return e
            '''
        ))
        self.entities = entities

    def get_arguments(self) -> dict:
        return {
            'props': [
                {
                    "mention": entity.mention,
                    "entity_source": entity.entity_source,
                    "entity_source_id": entity.entity_source_id,
                    "has_mention_vector": entity.has_mention_vector,
                    "mention_vector": entity.mention_vector.tolist()
                } for entity in self.entities
            ]
        }

    def consume(self, result: list[Record]) -> dict:
        return {'entities': [Neo4JEntity.from_dict(record['e']) for record in result]}
