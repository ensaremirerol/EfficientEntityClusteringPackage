from eec.interfaces.interface_entity_repository.i_entity_repository import IEntityRepository
from eec.implementations.neo4j.models.neo4j_entity import Neo4JEntity
from eec.exceptions.general.exceptions import *

import gensim
import numpy as np
from typing import Optional, cast
from neo4j import Driver

import logging


class Neo4JEntityRepository(IEntityRepository):
    def __init__(self,
                 driver: Driver,
                 keyed_vectors: gensim.models.Word2Vec):
        super().__init__()
        self.keyed_vectors = keyed_vectors
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    # region Queries
    @staticmethod
    def _get_entity_by_id(tx, id):
        query = "MATCH (e:Entity) WHERE e.entity_id = $id RETURN e"
        result = tx.run(query, id=id)
        return result.single()

    @staticmethod
    def _get_entity_by_mention(tx, mention):
        query = "MATCH (e:Entity) WHERE e.mention = $mention RETURN e"
        result = tx.run(query, mention=mention)
        return result.single()

    @staticmethod
    def _get_entities_by_source(tx, source):
        query = "MATCH (e:Entity) WHERE e.entity_source = $source RETURN e"
        result = tx.run(query, source=source)
        return [record["e"] for record in result]

    @staticmethod
    def _get_entity_by_source_id(tx, source, source_id):
        query = "MATCH (e:Entity) WHERE e.entity_source = $source AND e.entity_source_id = $source_id RETURN e"
        result = tx.run(query, source=source, source_id=source_id)
        return result.single()

    @staticmethod
    def _get_all_entities(tx):
        query = "MATCH (e:Entity) RETURN e"
        result = tx.run(query)
        return [record["e"] for record in result]

    @staticmethod
    def _create_entity(tx, mention: str, entity_source: str, entity_source_id: str,
                       has_mention_vector: bool, mention_vector: list):
        query = '''
            CREATE (entity:Entity {
                entity_id: apoc.create.uuid(),
                mention: $mention,
                entity_source: $entity_source,
                entity_source_id: $entity_source_id,
                in_cluster: false,
                cluster_id: '',
                has_mention_vector: $has_mention_vector,
                mention_vector: $mention_vector
            }) RETURN entity
        '''
        result = tx.run(query, mention=mention, entity_source=entity_source,
                        entity_source_id=entity_source_id, has_mention_vector=has_mention_vector,
                        mention_vector=mention_vector)
        return result.single()

    @staticmethod
    def _create_entities(tx, entities: list[Neo4JEntity]):
        props = [
            {
                "mention": entity.mention,
                "entity_source": entity.entity_source,
                "entity_source_id": entity.entity_source_id,
                "in_cluster": False,
                "cluster_id": '',
                "has_mention_vector": entity.has_mention_vector,
                "mention_vector": entity.mention_vector.tolist()
            } for entity in entities
        ]

        query = '''
            UNWIND $props AS prop
            CREATE (entity:Entity {
                entity_id: apoc.create.uuid(),
                mention: prop.mention,
                entity_source: prop.entity_source,
                entity_source_id: prop.entity_source_id,
                in_cluster: prop.in_cluster,
                cluster_id: prop.cluster_id,
                has_mention_vector: prop.has_mention_vector,
                mention_vector: prop.mention_vector
            }) return entity
        '''

        result = tx.run(query, props=props)
        return [cast(Neo4JEntity, Neo4JEntity.from_dict(entity['entity'])) for entity in result]

    @staticmethod
    def _delete_entity_by_id(tx, id):
        query = "MATCH (e:Entity) WHERE e.entity_id = $id DETACH DELETE e"
        result = tx.run(query, id=id)
        return result.single()

    @staticmethod
    def _delete_entities_by_ids(tx, ids):
        query = "MATCH (e:Entity) WHERE e.entity_id IN $ids DETACH DELETE e"
        result = tx.run(query, ids=ids)

    @staticmethod
    def _delete_all_entities(tx):
        query = "MATCH (e:Entity) DETACH DELETE e"
        result = tx.run(query)

    @staticmethod
    def _get_random_unclustered_entity(tx):
        query = "MATCH (e:Entity) WITH e, rand() AS r WHERE e.in_cluster = false RETURN e ORDER BY r LIMIT 1"
        result = tx.run(query)
        return result.single()

    @staticmethod
    def _get_random_unclustered_entities(tx, n):
        query = "MATCH (e:Entity) WITH e, rand() AS r WHERE e.in_cluster = false RETURN e ORDER BY r LIMIT $n"
        result = tx.run(query, n=n)
        return [record["e"] for record in result]

    @staticmethod
    def _update_entity(tx, entity: Neo4JEntity):
        query = '''
            MATCH (e:Entity) WHERE e.entity_id = $id
            SET e.mention = $mention,
                e.entity_source = $entity_source,
                e.entity_source_id = $entity_source_id,
                e.in_cluster = $in_cluster,
                e.cluster_id = $cluster_id,
                e.has_mention_vector = $has_mention_vector,
                e.mention_vector = $mention_vector
            RETURN e
        '''
        result = tx.run(
            query, id=entity.entity_id, mention=entity.mention, entity_source=entity.entity_source,
            entity_source_id=entity.entity_source_id, in_cluster=entity.in_cluster,
            cluster_id=entity.cluster_id, has_mention_vector=entity.has_mention_vector,
            mention_vector=entity.mention_vector.tolist())
        return result.single()

    @staticmethod
    def _update_entities(tx, entities: list[Neo4JEntity]):
        props = [
            {
                "id": entity.entity_id,
                "mention": entity.mention,
                "entity_source": entity.entity_source,
                "entity_source_id": entity.entity_source_id,
                "in_cluster": entity.in_cluster,
                "cluster_id": entity.cluster_id,
                "has_mention_vector": entity.has_mention_vector,
                "mention_vector": entity.mention_vector.tolist()
            } for entity in entities
        ]

        query = '''
            UNWIND $props AS prop
            MATCH (e:Entity) WHERE e.entity_id = prop.id
            SET e.mention = prop.mention,
                e.entity_source = prop.entity_source,
                e.entity_source_id = prop.entity_source_id,
                e.in_cluster = prop.in_cluster,
                e.cluster_id = prop.cluster_id,
                e.has_mention_vector = prop.has_mention_vector,
                e.mention_vector = prop.mention_vector
            RETURN e
        '''
        result = tx.run(query, props=props)
        return [cast(Neo4JEntity, Neo4JEntity.from_dict(entity['e'])) for entity in result]

    # endregion

    def get_entity_by_id(self, entity_id: str) -> Neo4JEntity:
        with self.driver.session() as session:
            result = session.execute_read(self._get_entity_by_id, entity_id)
            if result is None:
                raise NotFoundException(f"Entity with id {entity_id} not found")
            return cast(Neo4JEntity, Neo4JEntity.from_dict(result["e"]))

    def get_entity_by_mention(self, mention: str) -> Neo4JEntity:
        with self.driver.session() as session:
            result = session.execute_read(self._get_entity_by_mention, mention)
            if result is None:
                raise NotFoundException(f"Entity with mention {mention} not found")
            return cast(Neo4JEntity, Neo4JEntity.from_dict(result["e"]))

    def get_entities_by_source(self, source: str) -> list[Neo4JEntity]:
        with self.driver.session() as session:
            result = session.execute_read(self._get_entities_by_source, source)
            return [cast(Neo4JEntity, Neo4JEntity.from_dict(entity)) for entity in result]

    def get_entity_by_source_id(self, source: str, source_id: str) -> Neo4JEntity:
        with self.driver.session() as session:
            result = session.execute_read(self._get_entity_by_source_id, source, source_id)
            if result is None:
                raise NotFoundException(
                    f"Entity with source {source} and source_id {source_id} not found")
            return cast(Neo4JEntity, Neo4JEntity.from_dict(result["e"]))

    def get_all_entities(self) -> list[Neo4JEntity]:
        with self.driver.session() as session:
            result = session.execute_read(self._get_all_entities)
            return [cast(Neo4JEntity, Neo4JEntity.from_dict(entity)) for entity in result]

    def add_entity(self, entity: Neo4JEntity) -> Neo4JEntity:
        self.calculate_entity_vector(entity)
        with self.driver.session() as session:
            result = session.execute_write(
                self._create_entity, entity.mention, entity.entity_source, entity.entity_source_id,
                entity.has_mention_vector, entity.mention_vector.tolist())
            return cast(Neo4JEntity, Neo4JEntity.from_dict(result["entity"]))

    def add_entities(self, entities: list[Neo4JEntity]):
        for entity in entities:
            self.calculate_entity_vector(entity)
        with self.driver.session() as session:
            result = session.execute_write(self._create_entities, entities)

    def delete_entity(self, entity_id: str) -> Neo4JEntity:
        with self.driver.session() as session:
            result = session.execute_write(self._delete_entity_by_id, entity_id)
            return cast(Neo4JEntity, Neo4JEntity.from_dict(result["e"]))

    def delete_entities(self, entity_ids: list[str]):
        with self.driver.session() as session:
            session.execute_write(self._delete_entities_by_ids, entity_ids)

    def is_in_repository(
            self, entity_id: Optional[str] = None, entity: Optional[Neo4JEntity] = None,
            entity_source: Optional[str] = None, entity_source_id: Optional[str] = None) -> bool:
        try:
            if entity is not None:
                return self.get_entity_by_id(entity.entity_id) is not None
            if entity_id is not None:
                return self.get_entity_by_id(entity_id) is not None
            if entity_source is not None and entity_source_id is not None:
                return self.get_entity_by_source_id(
                    entity_source, entity_source_id) is not None
        except NotFoundException:
            return False

        if (entity_source is None and entity_source_id is not None) or (entity_source is not None and entity_source_id is None):
            raise ArgumentException("You must provide both entity_source and entity_source_id")

        raise ArgumentException(
            "You must provide at least one of the following: entity_id, entity or both entity_source and entity_source_id")

    def delete_all_entities(self):
        with self.driver.session() as session:
            session.execute_write(self._delete_all_entities)

    def update_entity(self, entity: Neo4JEntity) -> Neo4JEntity:
        self.calculate_entity_vector(entity)
        with self.driver.session() as session:
            result = session.execute_write(
                self._update_entity, entity)
            return cast(Neo4JEntity, Neo4JEntity.from_dict(result["entity"]))

    def update_entities(self, entities: list[Neo4JEntity]):
        with self.driver.session() as session:
            result = session.execute_write(self._update_entities, entities)

    def get_random_unlabeled_entity(self) -> Neo4JEntity:
        with self.driver.session() as session:
            result = session.execute_read(self._get_random_unclustered_entity)
            if result is None:
                raise NotFoundException("No unlabeled entities found")
            return cast(Neo4JEntity, Neo4JEntity.from_dict(result["e"]))

    def get_random_unlabeled_entities(self, count: int) -> list[Neo4JEntity]:
        with self.driver.session() as session:
            result = session.execute_read(self._get_random_unclustered_entities, count)
            return [cast(Neo4JEntity, Neo4JEntity.from_dict(entity)) for entity in result]

    def calculate_entity_vector(self, entity: Neo4JEntity):
        vecs = [
            self.keyed_vectors.wv[word] for word in entity.mention.split()
            if word in self.keyed_vectors.wv.key_to_index]
        if len(vecs) == 0:
            entity.has_mention_vector = False
            entity.mention_vector = np.zeros(self.keyed_vectors.vector_size)
            return

        entity.has_mention_vector = True
        entity.mention_vector = np.mean(vecs, axis=0)

    def calculate_all_entity_vectors(self):
        entities = self.get_all_entities()
        for entity in entities:
            self.calculate_entity_vector(entity)
        self.update_entities(entities)

    def get_all_entities_in_cluster(self,) -> list[Neo4JEntity]:
        entities = self.get_all_entities()
        return [entity for entity in entities if entity.in_cluster]

    def to_dict(self) -> dict:
        return {
            "entities": [entity.to_dict() for entity in self.get_all_entities()],
        }
