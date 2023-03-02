from typing import Optional


class EntityModel():
    def __init__(
            self, mention: str, entity_id: str, entity_source: str, entity_source_id: str,
            cluster_id: Optional[str] = None,
            has_cluster: bool = False,
            mention_vector: list[float] = [],
            has_mention_vector: bool = False,):
        self.mention: str = mention
        self.entity_id: str = entity_id
        self.entity_source: str = entity_source
        self.entity_source_id: str = entity_source_id
        self.cluster_id: Optional[str] = cluster_id
        self.has_cluster: bool = has_cluster
        self.mention_vector: list[float] = mention_vector
        self.has_mention_vector: bool = has_mention_vector

    def __str__(self):
        return f"EntityModel({self.mention}, {self.entity_id})"

    def __repr__(self):
        return f"EntityModel({self.mention}, {self.entity_id})"

    def __eq__(self, other):
        if not isinstance(other, EntityModel):
            return False
        return self.entity_id == other.entity_id

    def __hash__(self):
        return hash(self.entity_id)

    def to_dict(self):
        return {
            "mention": self.mention,
            "entity_id": self.entity_id,
            "entity_source": self.entity_source,
            "entity_source_id": self.entity_source_id,
            "cluster_id": self.cluster_id,
            "has_cluster": self.has_cluster,
            "mention_vector": self.mention_vector,
            "has_mention_vector": self.has_mention_vector,
        }

    @classmethod
    def from_dict(cls, map: dict) -> 'EntityModel':
        return EntityModel(
            map["mention"], map["entity_id"], map["entity_source"], map["entity_source_id"],
            map["cluster_id"], map["has_cluster"], map["mention_vector"], map["has_mention_vector"],
        )
