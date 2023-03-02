from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import ClusterModel, EntityModel, UserModel


class Neo4J_SetClusterVectorHelper(INeo4JQueryHelper):
    """
    Sets the cluster vector for a cluster
    Returns None if the cluster does not exist

    params:
        cluster_id: str
        cluster_vector: list[float]

    returns:
        {
            'cluster': ClusterModel | None (without entities)
        }

    """

    def __init__(self, cluster_id: str, cluster_vector: list[float]):
        super().__init__(
            name='set_cluster_vector',
            query=Query('''
                MATCH (c:Cluster {cluster_id: $cluster_id})
                SET c.cluster_vector = $cluster_vector
                RETURN c
            ''')
        )
        self.cluster_id = cluster_id
        self.cluster_vector = cluster_vector

    def get_arguments(self) -> dict:
        return {'cluster_id': self.cluster_id, 'cluster_vector': self.cluster_vector}

    def consume(self, result: list[Record]) -> dict:
        if len(result) != 1:
            return {'cluster': None}
        return {'cluster': ClusterModel.from_dict_separate_entities(result[0]['c'], entities=[])}
