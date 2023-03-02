from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import EntityModel


class Neo4J_GetEntityByMentionHelper(INeo4JQueryHelper):
    """
    Gets an entity by its mention.
    Returns None if no entity is found.

    params:
        mention: str

    returns:
        {
            'entity': EntityModel | None
        }
    """

    def __init__(self, mention: str):
        super().__init__(
            'get_entity_by_mention',
            query=Query('''
            MATCH (e:Entity {mention: $mention})
            OPTIONAL MATCH (c:Cluster)-[:HAS_ENTITY]->(e)
            SET e.cluster_id = COALESCE(c.cluster_id, null)
            SET e.has_cluster = COALESCE(c.cluster_id IS NOT NULL, false)
            RETURN e
            ''')
        )
        self.mention = mention

    def get_arguments(self) -> dict:
        return {'mention': self.mention}

    def consume(self, result: list[Record]) -> dict:
        return {
            'entity': EntityModel.from_dict(result[0]['e']) if len(result) == 1 else None
        }
