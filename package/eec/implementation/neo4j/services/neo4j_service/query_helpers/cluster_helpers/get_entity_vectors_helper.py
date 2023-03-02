from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import ClusterModel, EntityModel, UserModel


class Neo4J_GetEntityVectorsHelper(INeo4JQueryHelper):
    """
    Gets all entity vectors from a cluster
    Returns None if cluster does not exist

    params:
        cluster_id: str

    returns:
        {
            'vectors': list[list[float]] | None
        }

    """

    def __init__(self, cluster_id: str):
        super().__init__(
            name='get_entity_vectors',
            query=Query('''
                MATCH (c:Cluster {cluster_id: $cluster_id})
                OPTIONAL MATCH (c)-[r:HAS_ENTITY]->(e:Entity)
                RETURN COLLECT(e.mention_vector) AS vectors
            ''')
        )
        self.cluster_id = cluster_id

    def get_arguments(self) -> dict:
        return {
            'cluster_id': self.cluster_id
        }

    def consume(self, result: list[Record]) -> dict:
        if len(result) == 0:
            return {'vectors': None}
        return {
            'vectors': result[0]['vectors']
        }
