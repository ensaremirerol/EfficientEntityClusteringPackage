from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import ClusterModel, EntityModel, UserModel


class Neo4J_UpdateClustersHelper(INeo4JQueryHelper):
    """
    Updates clusters

    params:
        clusters: list[ClusterModel]

    returns:
        {
            'clusters': list[ClusterModel]
        }

    """

    def __init__(self, clusters: list[ClusterModel]):
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
                'cluster_vector': cluster.cluster_vector
            } for cluster in self.clusters]}

    def consume(self, result: list[Record]) -> dict:
        if len(result) == 0:
            return {'clusters': None}
        return {
            'clusters': [ClusterModel.from_dict_separate_entities(record['c'], entities=[
                EntityModel.from_dict(entity) for entity in record['e']
            ]) for record in result]
        }
