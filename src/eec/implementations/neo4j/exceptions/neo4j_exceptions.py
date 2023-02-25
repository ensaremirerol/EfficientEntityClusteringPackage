class Neo4J_DoNotUseThisException(Exception):
    def __init__(self, message: str):
        super().__init__(message)