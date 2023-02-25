from neo4j import GraphDatabase
from eec.implementations.neo4j.neo4j_services.query_helpers.i_neo4j_query_helper import INeo4JQueryHelper

# singleton


class Neo4JHelper():
    """Singleton class for Neo4J database connection."""
    _instance = None

    @staticmethod
    def get_instance():
        """Static access method"""
        if Neo4JHelper._instance is None:
            raise Exception("Neo4JHelper not initialized")
        return Neo4JHelper._instance

    def __init__(self, uri: str, user: str, password: str):
        """
            params:
                uri: the bolt uri of the Neo4J database
                user: the username of the Neo4J database
                password: the password of the Neo4J database
        """
        if Neo4JHelper._instance is not None:
            print("Neo4JHelper already initialized")
            print("To reinitialize, call Neo4JHelper.close() first")
            return
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        Neo4JHelper._instance = self

    def close(self):
        self._driver.close()
        Neo4JHelper._instance = None

    def run_query(self, query_helper: INeo4JQueryHelper) -> dict:
        """Runs the given query helper and returns the result."""
        with self._driver.session() as session:
            result = session.run(query_helper.query, query_helper.get_arguments())
            data = list(result)
            return query_helper.consume(data)
