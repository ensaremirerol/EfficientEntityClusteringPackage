from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_GetClusterOfEntitiesHelper(INeo4JQueryHelper):
    """
    Gets the cluster of an entity.

    params:
        entity_id: the id of the entity

    returns:
        {
            'entity': Neo4JEntity | None,
            'cluster': Neo4JCluster (without entities) | None
        }
    """

    def __init__(self, entity_ids: list[str]):
        super().__init__(
            name='get_cluster_of_entities',
            query=Query('''
                UNWIND $entity_ids AS entity_id
                MATCH (c:Cluster)-[r:HAS_ENTITY]->(e:Entity {entity_id: entity_id})
                RETURN e, c
            ''')
        )
        self.entity_ids = entity_ids

    def get_arguments(self) -> dict:
        return {
            'entity_ids': self.entity_ids
        }

    def consume(self, result: list[Record]) -> dict:
        if len(result) == 0:
            return {'clusters': [], 'entities': []}
        return {
            'clusters': [Neo4JCluster.from_dict(record['c'], []) for record in result],
            'entities': [Neo4JEntity.from_dict(record['e']) for record in result]
        }
