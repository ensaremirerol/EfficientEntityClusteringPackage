from eec.implementation.neo4j.services.neo4j_service.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.core.data_model import UserModel


class Neo4J_CreateUserHelper(INeo4JQueryHelper):
    """
    Creates a user.
    Returns None if user already exists.

    params:
        user: UserModel

    returns:
        {
            'user': UserModel | None
        }
    """

    def __init__(self, user: UserModel):
        super().__init__(
            'get_user_by_username',
            query=Query('''
                CREATE (user:User {
                    user_id: apoc.create.uuid(),
                    username: $username,
                    role: $role,
                    hashed_password: $hashed_password
                })
                RETURN user
            ''')
        )
        self.user = user

    def get_arguments(self) -> dict:
        return {
            'username': self.user.username,
            'role': self.user.role,
            'hashed_password': self.user.hashed_password
        }

    def consume(self, result: list[Record]) -> dict:
        return {
            'user': UserModel.from_dict(result[0]['user']) if len(result) == 1 else None
        }
