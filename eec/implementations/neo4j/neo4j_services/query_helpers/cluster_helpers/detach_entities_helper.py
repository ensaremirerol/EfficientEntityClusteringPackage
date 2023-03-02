from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_DetachEntitiesHelper(INeo4JQueryHelper):
    """
        Deletes all relationships of given entities to clusters

        params:
            cluster_id: str
            entity_ids: list[str]

        returns:
            {
                'changes': int,
                'objects': list[{
                    'entity': Neo4JEntity,
                    'cluster': Neo4JCluster
                }]
            }

    """

    def __init__(self, cluster_id: str, entity_ids: list[str]):
        super().__init__(
            name='detach_entities',
            query=Query('''
                UNWIND $props AS prop
                MATCH (c:Cluster {cluster_id: prop.cluster_id})-[r:HAS_ENTITY]->(e:Entity {entity_id: prop.entity_id})
                DELETE r
                RETURN e, c
            ''')
        )
        self.entity_ids = entity_ids
        self.cluster_id = cluster_id

    def get_arguments(self) -> dict:
        return {
            'props': [
                {
                    'cluster_id': self.cluster_id,
                    'entity_id': entity_id
                } for entity_id in self.entity_ids
            ]
        }

    def consume(self, result: list[Record]) -> dict:
        if len(result) == 0:
            return {'entity': None, 'cluster': None}
        return {
            'changes': len(result),
            'objects': [
                {
                    'entity': Neo4JEntity.from_dict(record['e']),
                    'cluster': Neo4JCluster.from_dict(record['c'], entities=[])
                } for record in result
            ]
        }
