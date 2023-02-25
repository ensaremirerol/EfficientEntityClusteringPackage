from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_GetClosestClustersHelper(INeo4JQueryHelper):
    """
    Gets the closest clusters to the vector.

    params:
        n: int - number of clusters to return
        vector: list[float] - vector to compare to

    returns:
        clusters: list[Neo4JCluster] - list of clusters
    """

    def __init__(self, n: int, vector: list[float]):
        super().__init__('get_closest_clusters', query=Query(
            '''
                MATCH (c:Cluster)-[:HAS_ENTITY]->(e:Entity)
                WHERE c.cluster_vector <> []
                WITH c, e, gds.similarity.cosine($vector, c.cluster_vector) AS similarity
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
                Neo4JCluster.from_dict(record['c'],
                                       entities=[Neo4JEntity.from_dict(entity)
                                                 for entity in record['e']] if record['e'] else [])
                for record in result
            ],
            'similarities': [record['similarity'] for record in result]
        }
