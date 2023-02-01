from src.interfaces.interface_entity.i_entity import IEntity

import numpy as np


class BaseEntity(IEntity):
    def __init__(
            self, mention: str, entity_id: str, entity_source: str, entity_source_id: str,
            in_cluster: bool = False, cluster_id: str = None, has_mention_vector: bool = False,
            mention_vector: np.ndarray = np.array([])):
        super().__init__(mention, entity_id, entity_source, entity_source_id, in_cluster, cluster_id)
        self.mention_vector: np.ndarray = mention_vector
        self.has_mention_vector: bool = has_mention_vector

    def get_mention_vector(self) -> np.ndarray:
        return self.mention_vector

    def distance_to(self, other: IEntity, distance_function: function) -> float:
        return distance_function(self.get_mention_vector(), other.get_mention_vector())

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

    @staticmethod
    def from_dict(map: dict) -> IEntity:
        mention_vector = np.array(
            map["mention_vector"]) if map["has_mention_vector"] else np.array(
            [])
        return BaseEntity(
            map["mention"], map["entity_id"], map["entity_source"], map["entity_source_id"],
            map["in_cluster"], map["cluster_id"], map["has_mention_vector"], mention_vector)

    def __str__(self):
        return f"{self.entity_id}-{self.mention}"

    def __repr__(self):
        return self.__str__()
