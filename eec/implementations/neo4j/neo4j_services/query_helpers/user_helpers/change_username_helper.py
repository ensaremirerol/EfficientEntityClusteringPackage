from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_user import Neo4JUser
from typing import Optional


class Neo4J_ChangeUsernameHelper(INeo4JQueryHelper):
    """
    Updates a user's username.
    Returns None if no user is found.

    params:
        user_id: str
        user_name: str

    returns:
        {
            'user': Neo4JUser | None
        }
    """

    def __init__(self, user_id: str, user_name: str):
        super().__init__(
            'update_user',
            query=Query('''
                MATCH (user:User {user_id: $user_id})
                SET user.user_name = $user_name
                RETURN user
            ''')
        )
        self.user_id = user_id
        self.user_name = user_name

    def get_arguments(self) -> dict:
        return {
            'user_id': self.user_id,
            'user_name': self.user_name
        }

    def consume(self, result: list[Record]) -> dict:
        return {
            'user': Neo4JUser.from_dict(result[0]['user']) if len(result) == 1 else None
        }
