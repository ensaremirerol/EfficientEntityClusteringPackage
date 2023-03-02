class Neo4J_DoNotUseThisException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Neo4J_QueryExecutionException(Exception):
    def __init__(self, query_name: str, exception: Exception):
        super().__init__(f"Query {query_name} failed: {exception}")
