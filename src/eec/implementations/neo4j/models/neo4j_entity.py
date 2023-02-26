from eec.interfaces.interface_entity.i_entity import IEntity
from eec.implementations.neo4j.exceptions.neo4j_exceptions import *

import numpy as np
from typing import Callable, Optional


class Neo4JEntity(IEntity):
    def __init__(
            self, mention: str, entity_id: str, entity_source: str, entity_source_id: str,
        cluster_id: Optional[str] = None,
            mention_vector: np.ndarray = np.array([]), has_mention_vector: bool = False):
        super().__init__(mention, entity_id, entity_source, entity_source_id, cluster_id is not None, cluster_id)
        self.mention_vector: np.ndarray = mention_vector
        self.has_mention_vector: bool = has_mention_vector
        self.priority: int = 0

    def set_cluster_id(self, cluster_id: Optional[str]):
        raise Neo4J_DoNotUseThisException(
            "Neo4J does not support setting the cluster id of an entity.\n Check for relationships instead."
        )

    def get_cluster_id(self) -> Optional[str]:
        return self.cluster_id

    def get_mention_vector(self) -> np.ndarray:
        return self.mention_vector

    def set_mention_vector(self, mention_vector: np.ndarray):
        self.mention_vector = mention_vector
        self.has_mention_vector = mention_vector != np.array([])

    def distance_to(
            self, other, distance_function: Callable[[np.ndarray, np.ndarray],
                                                     float]) -> float:
        return distance_function(self.get_mention_vector(), other.get_mention_vector())

    def lower_priority(self):
        self.priority += 1

    def reset_priority(self):
        self.priority = 0

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "entity_source": self.entity_source,
            "entity_source_id": self.entity_source_id,
            "mention": self.mention,
            "in_cluster": self.in_cluster,
            "cluster_id": self.cluster_id,
            "has_mention_vector": self.has_mention_vector,
            "mention_vector": self.mention_vector.tolist()
        }

    @classmethod
    def from_dict(cls, map: dict) -> 'Neo4JEntity':
        mention_vector = np.asarray(map["mention_vector"])
        return Neo4JEntity(
            map["mention"], map["entity_id"], map["entity_source"], map["entity_source_id"],
            map["cluster_id"], mention_vector, map["has_mention_vector"])

    def __str__(self):
        return f"{self.entity_id}-{self.mention}"

    def __repr__(self):
        return self.__str__()
