from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import ClusterModel, EntityModel, UserModel


class Neo4J_DetachClusterFromEntityHelper(INeo4JQueryHelper):
    """
        Deletes the relationship between a cluster and an entity
        Returns None if the cluster or entity does not exist

        params:
            entity_id: str

        returns:
            {
                'entity': EntityModel | None,
                'cluster': ClusterModel | None (without entities)
            }

    """

    def __init__(self, entity_id: str):
        super().__init__(
            name='detach_cluster_from_entity',
            query=Query('''
                MATCH (c:Cluster)-[r:HAS_ENTITY]->(e:Entity {entity_id: $entity_id})
                DELETE r
                RETURN e, c
            ''')
        )
        self.entity_id = entity_id

    def get_arguments(self) -> dict:
        return {
            'entity_id': self.entity_id,
        }

    def consume(self, result: list[Record]) -> dict:
        if len(result) != 1:
            return {'entity': None, 'cluster': None}
        return {
            'entity': EntityModel.from_dict(result[0]['e']),
            'cluster': ClusterModel.from_dict_separate_entities(result[0]['c'], entities=[])
        }
