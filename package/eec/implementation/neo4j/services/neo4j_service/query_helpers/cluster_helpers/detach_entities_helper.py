from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import ClusterModel, EntityModel, UserModel


class Neo4J_DetachEntitiesHelper(INeo4JQueryHelper):
    """
        Deletes all relationships of given entities to clusters

        params:
            entity_ids: list[str]

        returns:
            {
                'changes': int,
                'objects': list[{
                    'entity': EntityModel,
                    'cluster': ClusterModel
                }]
            }

    """

    def __init__(self, entity_ids: list[str]):
        super().__init__(
            name='detach_entities',
            query=Query('''
                UNWIND $props AS prop
                MATCH (c:Cluster)-[r:HAS_ENTITY]->(e:Entity {entity_id: prop.entity_id})
                DELETE r
                RETURN e, c
            ''')
        )
        self.entity_ids = entity_ids

    def get_arguments(self) -> dict:
        return {
            'props': [
                {
                    'entity_id': entity_id
                } for entity_id in self.entity_ids
            ]
        }

    def consume(self, result: list[Record]) -> dict:
        if len(result) == 0:
            return {'entity': None, 'cluster': None}
        return {
            'changes': len(result),
            'objects': [
                {
                    'entity': EntityModel.from_dict(record['e']),
                    'cluster': ClusterModel.from_dict_separate_entities(record['c'], entities=[])
                } for record in result
            ]
        }
