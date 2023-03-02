from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import ClusterModel, EntityModel, UserModel


class Neo4J_GetClusterOfEntitiesHelper(INeo4JQueryHelper):
    """
    Gets the cluster of an entity.

    params:
        entity_id: the id of the entity

    returns:
        {
            'entity': EntityModel | None,
            'cluster': ClusterModel (without entities) | None
        }
    """

    def __init__(self, entity_ids: list[str]):
        super().__init__(
            name='get_cluster_of_entities',
            query=Query('''
                UNWIND $entity_ids AS entity_id
                MATCH (c:Cluster)-[r:HAS_ENTITY]->(e:Entity {entity_id: entity_id})
                RETURN e, c
            ''')
        )
        self.entity_ids = entity_ids

    def get_arguments(self) -> dict:
        return {
            'entity_ids': self.entity_ids
        }

    def consume(self, result: list[Record]) -> dict:
        if len(result) == 0:
            return {'clusters': [], 'entities': []}
        return {
            'clusters': [ClusterModel.from_dict_separate_entities(record['c'], []) for record in result],
            'entities': [EntityModel.from_dict(record['e']) for record in result]
        }
