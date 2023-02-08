import unittest

from src.eec.implementations.base.models.base_cluster import BaseEntity
from src.eec.implementations.base.repositories.base_entity_repository import BaseEntityRepository

from src.eec.exceptions.general.exceptions import *

import numpy as np
import gensim

from typing import cast


class TestBaseEntityRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.entities = [
            BaseEntity(
                f'mention{i}', str(i),
                'source', str(i),
                None, np.random.rand(10)) for i in range(10)]
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
            last_id=10
        )

        self.entity_repository.calculate_all_entity_vectors()

    def test_get_entity_by_id(self) -> None:
        self.assertEqual(
            self.entity_repository.get_entity_by_id('1'),
            self.entities[1]
        )

    def test_get_entity_by_mention(self) -> None:
        self.assertEqual(
            self.entity_repository.get_entity_by_mention('mention1'),
            self.entities[1]
        )

    def test_get_entity_by_source_id(self) -> None:
        self.assertEqual(
            self.entity_repository.get_entity_by_source_id('source', '1'),
            self.entities[1]
        )

    def test_get_entities_by_source(self) -> None:
        self.assertEqual(
            self.entity_repository.get_entities_by_source('source'),
            self.entities
        )

    def test_get_all_entities(self) -> None:
        self.assertEqual(
            self.entity_repository.get_all_entities(),
            self.entities
        )

    def test_update_entity(self) -> None:
        entity = self.entities[1]
        entity.mention = 'test'
        self.entity_repository.update_entity(entity=entity)
        self.assertEqual(
            self.entity_repository.get_entity_by_id('1').mention,
            'test'
        )
        self.assertTrue(np.equal(self.entity_repository.get_entity_by_id(
            '1').mention_vector, self.keyed_vectors['test']).all())

    def test_add_entities(self) -> None:
        entity = BaseEntity(
            'test', '11',
            'source', '11',
            None, np.random.rand(10))
        self.entity_repository.add_entities([entity])
        self.assertEqual(
            self.entity_repository.get_entity_by_id('11'),
            entity
        )
        self.assertTrue(np.equal(self.entity_repository.get_entity_by_id(
            '11').mention_vector, self.keyed_vectors['test']).all())

    def test_delete_entity(self) -> None:
        self.entity_repository.delete_entity('1')
        with self.assertRaises(NotFoundException):
            self.entity_repository.get_entity_by_id('1')

    def test_is_in_repository(self) -> None:
        self.assertTrue(self.entity_repository.is_in_repository('1'))
        self.assertFalse(self.entity_repository.is_in_repository('11'))

    def test_delete_all_entities(self) -> None:
        self.entity_repository.delete_all_entities()
        self.assertEqual(self.entity_repository.get_all_entities(), [])

    def test_get_random_unlabelled_entity(self) -> None:
        for entity in self.entities[:-1]:
            entity.in_cluster = True
        entity = self.entity_repository.get_random_unlabeled_entities(1)[0]
        self.assertFalse(entity.in_cluster)
