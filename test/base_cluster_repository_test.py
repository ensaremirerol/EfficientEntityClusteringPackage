import unittest

from src.implementations.base.models.base_cluster import BaseEntity
from src.implementations.base.models.base_cluster import BaseCluster
from src.implementations.base.repositories.base_entity_repository import BaseEntityRepository
from src.implementations.base.repositories.base_cluster_repository import BaseClusterRepository
from src.exceptions.general.exceptions import *

import numpy as np
import gensim

from typing import cast


class TestBaseClusterRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.entities = [
            BaseEntity(
                f'mention{i}', str(i),
                'source', str(i),
                None, np.random.rand(10)) for i in range(100)]
        self.keyed_vectors = gensim.models.KeyedVectors(10)
        self.keyed_vectors.add_vectors(
            [entity.mention for entity in self.entities],
            [np.random.rand(10) for _ in range(10)]
        )
        self.keyed_vectors.add_vector(
            'test',
            np.random.rand(10)
        )

        self.entity_repository = BaseEntityRepository(
            entities=self.entities,
            keyed_vectors=self.keyed_vectors,
            last_id=100
        )

        self.clusters = [
            BaseCluster(
                cluster_id=str(i),
                cluster_name=f'cluster{i}', entities=[])
            for i in range(10)]

        self.cluster_repository = BaseClusterRepository(
            clusters=self.clusters,
            entity_repository=self.entity_repository,
            last_cluster_id=10
        )
