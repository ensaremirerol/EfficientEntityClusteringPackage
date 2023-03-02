from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import UserModel


class Neo4J_GetUserByUsernameHelper(INeo4JQueryHelper):
    """
    Gets a user by its username.
    Returns None if no user is found.

    params:
        username: str

    returns:
        {
            'user': UserModel | None
        }
    """

    def __init__(self, username: str):
        super().__init__(
            'get_user_by_username',
            query=Query('''
                MATCH (user:User {username: $username})
                RETURN user
            ''')
        )
        self.username = username

    def get_arguments(self) -> dict:
        return {'username': self.username}

    def consume(self, result: list[Record]) -> dict:
        return {
            'user': UserModel.from_dict(result[0]['user']) if len(result) == 1 else None
        }
