from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import ClusterModel, EntityModel, UserModel


class Neo4J_GetClosestClustersHelper(INeo4JQueryHelper):
    """
    Gets the closest clusters to the vector.

    params:
        n: int - number of clusters to return
        vector: list[float] - vector to compare to

    returns:
        clusters: list[ClusterModel] - list of clusters
    """

    def __init__(self, n: int, vector: list[float]):
        super().__init__('get_closest_clusters', query=Query(
            '''
                MATCH (c:Cluster)-[:HAS_ENTITY]->(e:Entity)
                WHERE c.cluster_vector <> []
                WITH c, e, gds.similarity.cosine($vector, c.cluster_vector) AS similarity
                SET e.cluster_id = COALESCE(c.cluster_id, null)
                SET e.in_cluster = COALESCE(c.cluster_id IS NOT NULL, false)
                RETURN c, COLLECT(e) AS e, similarity ORDER BY similarity DESC LIMIT $n
            '''
        ))
        self.n = n
        self.vector = vector

    def get_arguments(self) -> dict:
        return {
            'n': self.n,
            'vector': self.vector
        }

    def consume(self, result: list[Record]) -> dict:
        return {
            'clusters': [
                ClusterModel.from_dict_separate_entities(record['c'],
                                                         entities=[EntityModel.from_dict(entity)
                                                                   for entity in record['e']] if record['e'] else [])
                for record in result
            ],
            'similarities': [record['similarity'] for record in result]
        }
