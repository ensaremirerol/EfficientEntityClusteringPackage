from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import UserModel
from typing import Optional


class Neo4J_ChangeUsernameHelper(INeo4JQueryHelper):
    """
    Updates a user's username.
    Returns None if no user is found.

    params:
        user_id: str
        username: str

    returns:
        {
            'user': UserModel | None
        }
    """

    def __init__(self, user_id: str, username: str):
        super().__init__(
            'update_user',
            query=Query('''
                MATCH (user:User {user_id: $user_id})
                SET user.username = $username
                RETURN user
            ''')
        )
        self.user_id = user_id
        self.username = username

    def get_arguments(self) -> dict:
        return {
            'user_id': self.user_id,
            'username': self.username
        }

    def consume(self, result: list[Record]) -> dict:
        return {
            'user': UserModel.from_dict(result[0]['user']) if len(result) == 1 else None
        }
