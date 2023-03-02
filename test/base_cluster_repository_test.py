import unittest

from eec import *

import numpy as np
import gensim

from typing import cast


class TestBaseClusterRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.entities = [
            EntityModel(
                mention=f'mention{i}', entity_id=f'{i}',
                entity_source='source', entity_source_id=f'{i}',
                mention_vector=np.random.rand(10).tolist()
            ) for i in range(100)]
        self.model = gensim.models.Word2Vec.load(
            'data/word2vec.model')

        self.entity_repository = BaseEntityRepository(
            entities=self.entities,
            keyed_vectors=self.model,
            last_id=100
        )

        self.clusters = [
            ClusterModel(
                cluster_id=str(i),
                cluster_name=f'cluster{i}', entities=[])
            for i in range(10)]

        self.cluster_repository = BaseClusterRepository(
            clusters=self.clusters,
            entity_repository=self.entity_repository,
            last_cluster_id=10
        )

    def test_get_cluster_by_id(self):
        cluster = self.cluster_repository.get_cluster_by_id('1')
        self.assertEqual(cluster.cluster_id, '1')

    def test_get_all_clusters(self):
        clusters = self.cluster_repository.get_all_clusters()
        self.assertEqual(self.clusters, clusters)

    def test_add_cluster(self):
        cluster = ClusterModel(
            cluster_id='0',
            cluster_name='test',
            entities=[]
        )
        self.cluster_repository.add_cluster(cluster)
        self.assertEqual(cluster.cluster_id, '10')

    def test_add_clusters(self):
        clusters = [
            ClusterModel(
                cluster_id=str(i+10),
                cluster_name=f'cluster{i+10}',
                entities=[]
            ) for i in range(10)
        ]
        self.cluster_repository.add_clusters(clusters)
        print(self.cluster_repository.get_all_clusters())
        self.assertEqual(self.cluster_repository.get_all_clusters()[10:], clusters)

    def test_delete_cluster(self):
        self.cluster_repository.delete_cluster('1')
        self.assertEqual(len(self.cluster_repository.get_all_clusters()), 9)
        with self.assertRaises(NotFoundException):
            self.cluster_repository.delete_cluster('1')

    def test_delete_all_clusters(self):
        self.cluster_repository.delete_all_clusters()
        self.assertEqual(len(self.cluster_repository.get_all_clusters()), 0)

    def test_add_entity_to_cluster(self):
        entity = self.entity_repository.get_entity_by_id('1')
        self.cluster_repository.add_entity_to_cluster('1', '1')
        self.assertEqual(
            self.cluster_repository.get_cluster_by_id('1').entities,
            [entity]
        )
        self.assertEqual(entity.cluster_id, '1')
        self.assertTrue(entity.has_cluster)

    def test_remove_entity_from_cluster(self):
        self.cluster_repository.add_entity_to_cluster('1', '1')
        self.cluster_repository.remove_entity_from_cluster('1',)
        self.assertEqual(
            self.cluster_repository.get_cluster_by_id('1').entities,
            []
        )
        entity = self.entity_repository.get_entity_by_id('1')
        self.assertEqual(entity.cluster_id, None)
        self.assertFalse(entity.has_cluster)

    def test_to_dict(self):
        for i in range(10):
            for j in range(10):
                self.cluster_repository.add_entity_to_cluster(str(i), str((i*10)+j))
        clusters_dict = self.cluster_repository.to_dict()
        self.assertEqual(clusters_dict['last_cluster_id'], 10)
        self.assertEqual(clusters_dict['clusters'], [cluster.to_dict()
                         for cluster in self.clusters])

    def test_from_dict(self):
        for i in range(10):
            for j in range(10):
                self.cluster_repository.add_entity_to_cluster(str(i), str((i*10)+j))
        clusters_dict = self.cluster_repository.to_dict()
        cluster_repository = cast(BaseClusterRepository, BaseClusterRepository.from_dict(
            clusters_dict, self.entity_repository))
        self.assertEqual(cluster_repository.clusters, self.cluster_repository.clusters)
        self.assertEqual(cluster_repository.last_cluster_id,
                         self.cluster_repository.last_cluster_id)
