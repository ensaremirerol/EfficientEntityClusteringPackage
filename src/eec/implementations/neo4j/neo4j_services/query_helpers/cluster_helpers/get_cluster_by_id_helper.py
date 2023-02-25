from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_cluster import Neo4JCluster
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity


class Neo4J_GetClusterByIdHelper(INeo4JQueryHelper):
    """
    Gets a cluster by id
    Returns None if no cluster is found

    params:
        cluster_id: str

    returns:
        {
            'cluster': Neo4JCluster | None
        }

    """

    def __init__(self, cluster_id: str):
        super().__init__(
            name='get_cluster_by_id',
            query=Query('''
                MATCH (c:Cluster {cluster_id: $cluster_id})
                OPTIONAL MATCH (c)-[:HAS_ENTITY]->(e:Entity)
                RETURN c, COLLECT(e) AS e
            ''')
        )
        self.cluster_id = cluster_id

    def get_arguments(self) -> dict:
        return {'cluster_id': self.cluster_id}

    def consume(self, result: list[Record]) -> dict:
        if len(result) != 1:
            return {'cluster': None}
        entities: list[Neo4JEntity] = [Neo4JEntity.from_dict(
            entity) for entity in result[0]['e']] if result[0]['e'] else []
        return {'cluster': Neo4JCluster.from_dict(result[0]['c'], entities=entities)}
