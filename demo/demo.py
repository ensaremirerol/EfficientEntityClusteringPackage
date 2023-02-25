import eec
import numpy as np
import gensim
import pandas as pd
from neo4j import GraphDatabase

keyed_vectors = gensim.models.KeyedVectors.load('./demo/data/word2vec.model')

eec.Neo4JHelper('bolt://localhost:7687', user='neo4j', password='test')

entity_repository = eec.Neo4JEntityRepository(
    keyed_vectors=keyed_vectors,
)

cluster_repository = eec.Neo4JClusterRepository(
    entity_repository=entity_repository,
)


mention_clustering_method = eec.Neo4JMentionClusteringMethod(
    name='neo4j_mention_clustering_method',
    entity_repository=entity_repository,
    cluster_repository=cluster_repository,
)


eec.EntityClustererBridge().set_cluster_repository(cluster_repository)
eec.EntityClustererBridge().set_entity_repository(entity_repository)
eec.EntityClustererBridge().set_mention_clustering_method(mention_clustering_method)

entity = eec.EntityClustererBridge().entity_repository.get_random_unlabeled_entity()


print(eec.EntityClustererBridge().mention_clustering_method.getPossibleClusters(entity))
