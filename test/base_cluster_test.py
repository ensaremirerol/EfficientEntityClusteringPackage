import unittest

from src.implementations.base.models.base_cluster import BaseEntity
from src.implementations.base.models.base_cluster import BaseCluster
from src.exceptions.general.exceptions import *

import numpy as np

from typing import cast


class TestBaseCluster(unittest.TestCase):
    def setUp(self) -> None:
        self.entities = [
            BaseEntity(
                f'mention{i}', str(i),
                'source', str(i),
                None, np.random.rand(10)) for i in range(10)]
        self.cluster = BaseCluster(
            '1',
            'cluster',
            self.entities,
        )

    def test_get_entities(self) -> None:
        self.assertEqual(self.cluster.get_entities(), self.entities)

    def test_get_entity_by_id(self) -> None:
        self.assertEqual(
            self.cluster.get_entity_by_id('1'),
            self.entities[1]
        )

    def test_get_entity_by_mention(self) -> None:
        self.assertEqual(
            self.cluster.get_entity_by_mention('mention1'),
            self.entities[1]
        )

    def test_get_entity_by_source_id(self) -> None:
        self.assertEqual(
            self.cluster.get_entity_by_source_id('source', '1'),
            self.entities[1]
        )

    def test_get_entities_by_source(self) -> None:
        self.assertEqual(
            self.cluster.get_entities_by_source('source'),
            self.entities
        )

    def test_is_in_cluster(self) -> None:
        self.assertTrue(self.cluster.is_in_cluster(entity=self.entities[1]))
        self.assertTrue(self.cluster.is_in_cluster(entity_id='1'))
        self.assertTrue(self.cluster.is_in_cluster(entity_source='source', entity_source_id='1'))
        with self.assertRaises(ArgumentException):
            self.cluster.is_in_cluster(entity_source='source')

    def test_add_entity(self) -> None:
        entity = BaseEntity(
            'mention11', '11',
            'source', '11',
            None, np.random.rand(10))
        self.cluster.add_entity(entity)
        self.assertEqual(self.cluster.get_entity_by_id('11'), entity)
        with self.assertRaises(AlreadyExistsException):
            self.cluster.add_entity(entity)

    def test_remove_entity(self) -> None:
        self.cluster.remove_entity(entity=self.entities[1])
        with self.assertRaises(NotFoundException):
            self.cluster.get_entity_by_id('1')
        self.cluster.remove_entity(entity_id='2')
        with self.assertRaises(NotFoundException):
            self.cluster.get_entity_by_id('2')
        self.cluster.remove_entity(entity_source='source', entity_source_id='3')
        with self.assertRaises(NotFoundException):
            self.cluster.get_entity_by_id('3')
        with self.assertRaises(ArgumentException):
            self.cluster.remove_entity(entity_source='source')

    def test_calculate_cluster_vector(self) -> None:
        self.cluster.calculate_cluster_vector()
        self.assertTrue(
            np.equal(
                self.cluster.cluster_vector, np.mean(
                    [entity.mention_vector for entity in self.entities],
                    axis=0)).all())

    def test_to_dict(self) -> None:
        cluster_dict = self.cluster.to_dict()
        self.assertEqual(cluster_dict['cluster_id'], '1')
        self.assertEqual(cluster_dict['cluster_name'], 'cluster')
        self.assertEqual(cluster_dict['cluster_vector'], self.cluster.cluster_vector.tolist())
        self.assertEqual(cluster_dict['entities'], [entity.entity_id for entity in self.entities])

    def test_from_dict(self) -> None:  # TODO: BaseEntityRepository
        pass
