from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import EntityModel


class Neo4J_GetEntitiesBySourceHelper(INeo4JQueryHelper):
    """
    Gets all entities which have the given source.
    Returns None if no entities are found.

    params:
        entity_source: str

    returns:
        {
            'entities': list[EntityModel] | None
        }
    """

    def __init__(self, entity_source: str):
        super().__init__(
            'get_entity_by_source',
            query=Query('''
            MATCH (e:Entity {entity_source: $source})
            OPTIONAL MATCH (c:Cluster)-[:HAS_ENTITY]->(e)
            SET e.cluster_id = COALESCE(c.cluster_id, null)
            SET e.has_cluster = COALESCE(c.cluster_id IS NOT NULL, false)
            RETURN e
            ''')
        )
        self.entity_source = entity_source

    def get_arguments(self) -> dict:
        return {'entity_source': self.entity_source}

    def consume(self, result: list[Record]) -> dict:
        return {
            'entities': [EntityModel.from_dict(record['e']) for record in result] if len(result) > 0 else []
        }
