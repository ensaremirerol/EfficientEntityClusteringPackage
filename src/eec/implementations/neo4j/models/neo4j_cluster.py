from eec.exceptions.general.exceptions import *

import numpy as np
from typing import Optional, Callable


class Neo4JCluster():

    def __init__(self, cluster_id: str,
                 cluster_name: str,
                 entities: list[str],
                 cluster_vector: np.ndarray = np.array([])):
        self.cluster_id = cluster_id
        self.cluster_name = cluster_name
        self.entities: list[str] = entities
        self.cluster_vector: np.ndarray = cluster_vector

    def to_dict(self) -> dict:
        '''Returns a dict representation of the cluster.'''
        return {
            "cluster_id": self.cluster_id,
            "cluster_name": self.cluster_name,
            "entities": [entity for entity in self.entities],
            "cluster_vector": self.cluster_vector.tolist()
        }

    @staticmethod
    def from_dict(cluster_dict: dict):
        '''Returns a cluster from a dict representation.'''
        return Neo4JCluster(cluster_dict["cluster_id"],
                            cluster_dict["cluster_name"],
                            cluster_dict["entities"],
                            np.array(cluster_dict["cluster_vector"]))

    def __str__(self):
        return f"Cluster {self.cluster_id}-{self.cluster_name}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.cluster_id == other.cluster_id

    def __hash__(self):
        return hash(self.cluster_id)
