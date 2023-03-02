from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper
from neo4j import Record, Query

from eec.implementations.neo4j.models.neo4j_user import Neo4JUser


class Neo4J_GetAllUsersHelper(INeo4JQueryHelper):
    """
    Gets all users.

    params:
        None

    returns:
        {
            'users': list[Neo4JUser]
        }
    """

    def __init__(self,):
        super().__init__(
            'get_user_by_id',
            query=Query('''
                MATCH (user:User)
                RETURN user
            ''')
        )

    def consume(self, result: list[Record]) -> dict:
        return {
            'users': [Neo4JUser.from_dict(record['user']) for record in result] if len(result) > 0 else []
        }
