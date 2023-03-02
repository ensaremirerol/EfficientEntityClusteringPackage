from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import ClusterModel, EntityModel, UserModel


class Neo4J_DeleteAllClustersHelper(INeo4JQueryHelper):
    """
    Deletes all clusters

    params:
        None

    returns:
        {
            'clusters': list[ClusterModel]
        }

    """

    def __init__(self):
        super().__init__(
            name='delete_all_clusters',
            query=Query('''
                MATCH (c:Cluster)
                DETACH DELETE c
                RETURN c
            ''')
        )

    def consume(self, result: list[Record]) -> dict:
        return {
            'clusters': [
                ClusterModel.from_dict_separate_entities(record['c'],
                                                         entities=[])
                for record in result
            ]
        }
