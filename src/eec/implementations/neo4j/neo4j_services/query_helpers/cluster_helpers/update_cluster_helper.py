from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_UpdateClusterHelper(INeo4JQueryHelper):
    """
    Updates a cluster
    Returns None if cluster does not exist

    params:
        cluster: Neo4JCluster

    returns:
        {
            'cluster': Neo4JCluster | None
        }

    """

    def __init__(self, cluster: Neo4JCluster):
        super().__init__(
            name='update_cluster',
            query=Query('''
                MATCH (c:Cluster {cluster_id: prop.cluster_id})
                SET c.cluster_name = $cluster_name
                SET c.cluster_vector = $cluster_vector
                OPTIONAL MATCH (c)-[:HAS_ENTITY]->(e:Entity)
                RETURN c, COLLECT(e) AS e
            ''')
        )
        self.cluster = cluster

    def get_arguments(self) -> dict:
        return {
            'cluster_id': self.cluster.cluster_id,
            'cluster_name': self.cluster.cluster_name,
            'cluster_vector': self.cluster.cluster_vector.tolist()
        }

    def consume(self, result: list[Record]) -> dict:
        if len(result) != 1:
            return {'cluster': None}
        entities: list[Neo4JEntity] = [Neo4JEntity.from_dict(
            entity) for entity in result[0]['e']] if result[0]['e'] else []
        return {'cluster': Neo4JCluster.from_dict(result[0]['c'], entities=entities)}
