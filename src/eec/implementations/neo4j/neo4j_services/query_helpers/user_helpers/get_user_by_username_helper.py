from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_user import Neo4JUser


class Neo4J_GetUserByUsernameHelper(INeo4JQueryHelper):
    """
    Gets a user by its username.
    Returns None if no user is found.

    params:
        username: str

    returns:
        {
            'user': Neo4JUser | None
        }
    """

    def __init__(self, username: str):
        super().__init__(
            'get_user_by_username',
            query=Query('''
                MATCH (user:User {user_name: $username})
                RETURN user
            ''')
        )
        self.username = username

    def get_arguments(self) -> dict:
        return {'username': self.username}

    def consume(self, result: list[Record]) -> dict:
        return {
            'user': Neo4JUser.from_dict(result[0]['user']) if len(result) == 1 else None
        }
