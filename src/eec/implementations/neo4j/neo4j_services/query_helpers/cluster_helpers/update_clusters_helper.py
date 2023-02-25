from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_UpdateClustersHelper(INeo4JQueryHelper):
    """
    Updates clusters

    params:
        clusters: list[Neo4JCluster]

    returns:
        {
            'clusters': list[Neo4JCluster]
        }

    """

    def __init__(self, clusters: list[Neo4JCluster]):
        super().__init__(
            name='update_clusters',
            query=Query('''
                UNWIND $props AS prop
                MATCH (c:Cluster {cluster_id: prop.cluster_id})
                SET c.cluster_name = prop.cluster_name
                SET c.cluster_vector = prop.cluster_vector
                OPTIONAL MATCH (c)-[:HAS_ENTITY]->(e:Entity)
                RETURN c, COLLECT(e) AS e
            ''')
        )
        self.clusters = clusters

    def get_arguments(self) -> dict:
        return {
            'props': [{
                'cluster_id': cluster.cluster_id,
                'cluster_name': cluster.cluster_name,
                'cluster_vector': cluster.cluster_vector.tolist()
            } for cluster in self.clusters]}

    def consume(self, result: list[Record]) -> dict:
        if len(result) == 0:
            return {'clusters': None}
        return {
            'clusters': [Neo4JCluster.from_dict(record['c'], entities=[
                Neo4JEntity.from_dict(entity) for entity in record['e']
            ]) for record in result]
        }
