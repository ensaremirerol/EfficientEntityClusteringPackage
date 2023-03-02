from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import UserModel


class Neo4J_DeleteUserHelper(INeo4JQueryHelper):
    """
    Deletes a user.
    Returns None if no user is found.

    params:
        user_id: str

    returns:
        {
            'user': UserModel | None
        }
    """

    def __init__(self, user_id: str):
        super().__init__(
            'get_user_by_username',
            query=Query('''
                MATCH (user:User {user_id: $user_id})
                DETACH DELETE user
                RETURN user
            ''')
        )
        self.user_id = user_id

    def get_arguments(self) -> dict:
        return {'user_id': self.user_id}

    def consume(self, result: list[Record]) -> dict:
        return {
            'user': UserModel.from_dict(result[0]['user']) if len(result) == 1 else None
        }
