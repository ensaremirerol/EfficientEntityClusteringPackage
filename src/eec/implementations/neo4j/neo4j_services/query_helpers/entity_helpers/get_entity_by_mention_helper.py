from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_GetEntityByMentionHelper(INeo4JQueryHelper):
    """
    Gets an entity by its mention.
    Returns None if no entity is found.

    params:
        mention: str

    returns:
        {
            'entity': Neo4JEntity | None
        }
    """

    def __init__(self, mention: str):
        super().__init__(
            'get_entity_by_mention',
            query=Query('''
            MATCH (e:Entity {mention: $mention})
            OPTIONAL MATCH (c:Cluster)-[:HAS_ENTITY]->(e)
            SET e.cluster_id = COALESCE(c.cluster_id, null)
            SET e.in_cluster = COALESCE(c.cluster_id IS NOT NULL, false)
            RETURN e
            ''')
        )
        self.mention = mention

    def get_arguments(self) -> dict:
        return {'mention': self.mention}

    def consume(self, result: list[Record]) -> dict:
        return {
            'entity': Neo4JEntity.from_dict(result[0]['e']) if len(result) == 1 else None
        }
