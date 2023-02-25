from abc import ABC, abstractmethod
from neo4j import Record, Query


class INeo4JQueryHelper(ABC):
    """Abstract class for all Neo4J query helpers. Defines the query, its arguments, and how to consume the result."""

    def __init__(
            self, name: str,
            query: Query,) -> None:
        self.name = name
        self.query = query

    def get_arguments(self) -> dict:
        return {}

    @abstractmethod
    def consume(self, result: list[Record]) -> dict:
        pass
