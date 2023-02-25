from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_DetachClusterFromEntityHelper(INeo4JQueryHelper):
    """
        Deletes the relationship between a cluster and an entity
        Returns None if the cluster or entity does not exist

        params:
            entity_id: str
            cluster_id: str

        returns:
            {
                'entity': Neo4JEntity | None,
                'cluster': Neo4JCluster | None (without entities)
            }

    """

    def __init__(self, entity_id: str, cluster_id: str):
        super().__init__(
            name='detach_cluster_from_entity',
            query=Query('''
                MATCH (c:Cluster {cluster_id: $cluster_id})-[r:HAS_ENTITY]->(e:Entity {entity_id: $entity_id})
                DELETE r
                RETURN e, c
            ''')
        )
        self.entity_id = entity_id
        self.cluster_id = cluster_id

    def get_arguments(self) -> dict:
        return {
            'entity_id': self.entity_id,
            'cluster_id': self.cluster_id
        }

    def consume(self, result: list[Record]) -> dict:
        if len(result) != 1:
            return {'entity': None, 'cluster': None}
        return {
            'entity': Neo4JEntity.from_dict(result[0]['e']),
            'cluster': Neo4JCluster.from_dict(result[0]['c'], entities=[])
        }
