from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import ClusterModel, EntityModel, UserModel


class Neo4J_DeleteClustersHelper(INeo4JQueryHelper):
    """
    Deletes clusters

    params:
        cluster_ids: list[str]

    returns:
        {
            'clusters': list[ClusterModel]
        }

    """

    def __init__(self, cluster_ids: list[str]):
        super().__init__(
            name='delete_clusters',
            query=Query('''
                UNWIND $cluster_ids AS cluster_id
                MATCH (c:Cluster {cluster_id: $cluster_id})
                DETACH DELETE c
                RETURN c
            ''')
        )
        self.cluster_ids = cluster_ids

    def get_arguments(self) -> dict:
        return {
            'cluster_ids': self.cluster_ids
        }

    def consume(self, result: list[Record]) -> dict:
        if len(result) == 0:
            return {'clusters': None}
        return {
            'clusters': [
                ClusterModel.from_dict_separate_entities(record['c'], entities=[])
                for record in result
            ]
        }
