from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_user import Neo4JUser


class Neo4J_CreateUserHelper(INeo4JQueryHelper):
    """
    Creates a user.
    Returns None if user already exists.

    params:
        user: Neo4JUser

    returns:
        {
            'user': Neo4JUser | None
        }
    """

    def __init__(self, user: Neo4JUser):
        super().__init__(
            'get_user_by_username',
            query=Query('''
                CREATE (user:User {
                    user_id: apoc.create.uuid(),
                    user_name: $user_name,
                    role: $role,
                    hashed_password: $hashed_password
                })
                RETURN user
            ''')
        )
        self.user = user

    def get_arguments(self) -> dict:
        return {
            'user_name': self.user.user_name,
            'role': self.user.role,
            'hashed_password': self.user.hashed_password
        }

    def consume(self, result: list[Record]) -> dict:
        return {
            'user': Neo4JUser.from_dict(result[0]['user']) if len(result) == 1 else None
        }
