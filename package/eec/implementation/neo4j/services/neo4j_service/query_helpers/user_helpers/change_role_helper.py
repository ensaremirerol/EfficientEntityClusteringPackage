from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import UserModel
from typing import Optional


class Neo4J_ChangeUserRoleHelper(INeo4JQueryHelper):
    """
    Updates a user's role.
    Returns None if no user is found.

    params:
        user_id: str
        user_role: str

    returns:
        {
            'user': UserModel | None
        }
    """

    def __init__(self, user_id: str, user_role: str):
        super().__init__(
            'update_user',
            query=Query('''
                MATCH (user:User {user_id: $user_id})
                SET user.user_role = $user_role
                RETURN user
            ''')
        )
        self.user_id = user_id
        self.user_role = user_role

    def get_arguments(self) -> dict:
        return {
            'user_id': self.user_id,
            'user_role': self.user_role
        }

    def consume(self, result: list[Record]) -> dict:
        return {
            'user': UserModel.from_dict(result[0]['user']) if len(result) == 1 else None
        }
