from eec.core.data_model.entity_model import EntityModel


class ClusterModel():

    def __init__(self, cluster_id: str,
                 cluster_name: str,
                 entities: list[EntityModel],
                 cluster_vector: list[float] = [],
                 has_cluster_vector: bool = False,):

        self.cluster_id: str = cluster_id
        self.cluster_name: str = cluster_name
        self.entities: list[EntityModel] = entities
        self.cluster_vector: list[float] = cluster_vector
        self.has_cluster_vector: bool = has_cluster_vector

    def __getitem__(self, key):
        return self.entities[key]

    def __len__(self):
        return len(self.entities)

    def __iter__(self):
        return iter(self.entities)

    def __contains__(self, item):
        return item in self.entities

    def __str__(self):
        return f"ClusterModel({self.cluster_id}, {self.cluster_name})"

    def __repr__(self):
        return f"ClusterModel({self.cluster_id}, {self.cluster_name})"

    def __eq__(self, other):
        if not isinstance(other, ClusterModel):
            return False
        return self.cluster_id == other.cluster_id

    def __hash__(self):
        return hash(self.cluster_id)

    def to_dict(self):
        return {
            "cluster_id": self.cluster_id,
            "cluster_name": self.cluster_name,
            "entities": [entity.to_dict() for entity in self.entities],
            "cluster_vector": self.cluster_vector,
            "has_cluster_vector": self.has_cluster_vector,
        }

    @classmethod
    def from_dict(cls, map: dict) -> 'ClusterModel':
        return ClusterModel(
            map["cluster_id"], map["cluster_name"],
            [EntityModel.from_dict(entity) for entity in map["entities"]],
            map["cluster_vector"], map["has_cluster_vector"],
        )

    @classmethod
    def from_dict_separate_entities(cls, map: dict, entities: list[EntityModel]) -> 'ClusterModel':
        return cls(
            map["cluster_id"], map["cluster_name"],
            entities,
            map["cluster_vector"], map["has_cluster_vector"],
        )
