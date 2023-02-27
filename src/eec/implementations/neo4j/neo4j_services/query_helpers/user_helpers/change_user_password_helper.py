from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_user import Neo4JUser
from typing import Optional


class Neo4J_ChangeUserPasswordHelper(INeo4JQueryHelper):
    """
    Updates a user's password.
    Returns None if no user is found.

    params:
        user: Neo4JUser

    returns:
        {
            'user': Neo4JUser | None
        }
    """

    def __init__(self, user_id: str, hashed_password: str, salt: str):
        super().__init__(
            'update_user',
            query=Query('''
                MATCH (user:User {user_id: $user_id})
                SET user.hashed_password = $hashed_password
                SET user.salt = $salt
                RETURN user
            ''')
        )
        self.user_id = user_id
        self.hashed_password = hashed_password
        self.salt = salt

    def get_arguments(self) -> dict:
        return {
            'user_id': self.user_id,
            'hashed_password': self.hashed_password,
            'salt': self.salt
        }

    def consume(self, result: list[Record]) -> dict:
        return {
            'user': Neo4JUser.from_dict(result[0]['user']) if len(result) == 1 else None
        }
