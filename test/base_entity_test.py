import unittest

from eec.implementations.base.models.base_cluster import BaseEntity

import numpy as np
from typing import cast


class TestBaseEntity(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestBaseEntity, self).__init__(*args, **kwargs)
        self.base_entity: BaseEntity = BaseEntity("test", "0", "test_source", "0")

    def setUp(self):
        self.base_entity = BaseEntity("test", "0", "test_source", "0")

    def test_get_entity_id(self):
        self.assertEqual(self.base_entity.get_entity_id(), "0")

    def test_get_mention(self):
        self.assertEqual(self.base_entity.get_mention(), "test")

    def test_get_entity_source(self):
        self.assertEqual(self.base_entity.get_entity_source(), "test_source")

    def test_get_entity_source_id(self):
        self.assertEqual(self.base_entity.get_entity_source_id(), "0")

    def test_get_mention_vector(self):
        self.assertTrue(np.equal(self.base_entity.get_mention_vector(), np.array([])).all())

    def test_set_mention_vector(self):
        self.base_entity.set_mention_vector(np.array([0, 1]))
        self.assertTrue(np.equal(self.base_entity.get_mention_vector(), np.array([0, 1])).all())
        self.assertTrue(self.base_entity.has_mention_vector)

    def test_set_cluster_id(self):
        self.base_entity.set_cluster_id("1")
        self.assertEqual(self.base_entity.get_cluster_id(), "1")
        self.assertEqual(self.base_entity.in_cluster, True)

    def test_to_distace(self):
        def distance_function(a: np.ndarray, b: np.ndarray) -> float:
            return np.linalg.norm(a - b).astype(float)
        self.base_entity.set_mention_vector(np.array([0, 1]))
        self.assertEqual(self.base_entity.distance_to(self.base_entity, distance_function), 0)

        other_entity: BaseEntity = BaseEntity(
            "test", "1", "test_source", "1", mention_vector=np.array([0, 2]))
        self.assertEqual(
            self.base_entity.distance_to(other_entity, distance_function),
            1)

    def test_to_dict(self):
        self.base_entity.set_cluster_id("1")
        self.base_entity.set_mention_vector(np.array([0, 1]))
        self.assertEqual(self.base_entity.to_dict(), {
            "entity_id": "0",
            "entity_source": "test_source",
            "entity_source_id": "0",
            "mention": "test",
            "in_cluster": True,
            "cluster_id": "1",
            "has_mention_vector": True,
            "mention_vector": [0, 1]
        })

    def test_from_dict(self):
        self.base_entity.set_cluster_id("1")
        self.base_entity.set_mention_vector(np.array([0, 1]))
        new_entity: BaseEntity = cast(BaseEntity, BaseEntity.from_dict(self.base_entity.to_dict()))

        self.assertEqual(new_entity.get_entity_id(), "0")
        self.assertEqual(new_entity.get_entity_source(), "test_source")
        self.assertEqual(new_entity.get_entity_source_id(), "0")
        self.assertEqual(new_entity.get_mention(), "test")
        self.assertEqual(new_entity.in_cluster, True)
        self.assertEqual(new_entity.get_cluster_id(), "1")
        self.assertEqual(new_entity.has_mention_vector, True)
        self.assertTrue(np.equal(new_entity.get_mention_vector(), np.array([0, 1])).all())
