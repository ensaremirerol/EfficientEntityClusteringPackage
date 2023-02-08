from eec.interfaces.interface_entity_repository.i_entity_repository import IEntityRepository
from eec.implementations.base.models.base_entity import BaseEntity
from eec.exceptions.general.exceptions import *

import gensim
import numpy as np
from typing import Optional, cast


class BaseEntityRepository(IEntityRepository):
    def __init__(self,
                 entities: list[BaseEntity],
                 last_id: int,
                 keyed_vectors: gensim.models.keyedvectors.KeyedVectors):
        super().__init__()
        self.keyed_vectors = keyed_vectors
        self.entities = entities
        self.last_id = last_id

    def get_entity_by_id(self, entity_id: str) -> BaseEntity:
        for entity in self.entities:
            if entity.entity_id == entity_id:
                return entity
        raise NotFoundException(f"Entity with id {entity_id} not found")

    def get_entity_by_mention(self, mention: str) -> BaseEntity:
        for entity in self.entities:
            if entity.mention == mention:
                return entity
        raise NotFoundException(f"Entity with mention {mention} not found")

    def get_entities_by_source(self, source: str) -> list[BaseEntity]:
        return [entity for entity in self.entities if entity.entity_source == source]

    def get_entity_by_source_id(self, source: str, source_id: str) -> BaseEntity:
        for entity in self.entities:
            if entity.entity_source == source and entity.entity_source_id == source_id:
                return entity
        raise NotFoundException(f"Entity with source {source} and source_id {source_id} not found")

    def get_all_entities(self) -> list[BaseEntity]:
        return [entity for entity in self.entities]

    def update_entity(self, entity: BaseEntity):
        for i in range(len(self.entities)):
            if self.entities[i].entity_id == entity.entity_id:
                self.entities[i] = entity
                self.calculate_entity_vector(entity)
                return
        raise NotFoundException(f"Entity with id {entity.entity_id} not found")

    def add_entities(self, entities: list[BaseEntity]):
        for entity in entities:
            if self.is_in_repository(
                    entity_source=entity.entity_source, entity_source_id=entity.entity_source_id):
                print(f"Entity with id {entity.entity_id} already exists! Skipping...")
                continue
            self.calculate_entity_vector(entity)
            self.last_id += 1
            entity.entity_id = str(self.last_id)
            self.entities.append(entity)

    def delete_entity(self, entity_id: str):
        for i in range(len(self.entities)):
            if self.entities[i].entity_id == entity_id:
                del self.entities[i]
                return
        raise NotFoundException(f"Entity with id {entity_id} not found")

    def delete_entities(self, entity_ids: list[str]):
        for entity_id in entity_ids:
            self.delete_entity(entity_id)

    def is_in_repository(
            self, entity_id: Optional[str] = None, entity: Optional[BaseEntity] = None,
            entity_source: Optional[str] = None, entity_source_id: Optional[str] = None) -> bool:
        try:
            if entity is not None:
                return entity in self.entities
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
        for entity in self.entities:
            del entity
        self.entities = []

    def get_random_unlabeled_entity(self) -> BaseEntity:
        for entity in self.entities:
            if not entity.in_cluster:
                return entity
        raise NotFoundException("No unlabeled entities found")

    def get_random_unlabeled_entities(self, count: int) -> list[BaseEntity]:
        unlabeled_entities = []
        i = -1
        while len(unlabeled_entities) < count:
            i += 1
            if i >= len(self.entities):
                break
            if not self.entities[i].in_cluster:
                unlabeled_entities.append(self.entities[i])
        if len(unlabeled_entities) == 0:
            raise NotFoundException("No unlabeled entities found")
        return unlabeled_entities

    def calculate_entity_vector(self, entity: BaseEntity):
        vecs = [self.keyed_vectors[word]
                for word in entity.mention.split() if word in self.keyed_vectors]
        if len(vecs) == 0:
            entity.has_mention_vector = False
            entity.mention_vector = np.zeros(self.keyed_vectors.vector_size)
            return

        entity.has_mention_vector = True
        entity.mention_vector = np.mean(vecs, axis=0)

    def calculate_all_entity_vectors(self):
        for entity in self.entities:
            self.calculate_entity_vector(entity)

    def get_all_entities_in_cluster(self,) -> list[BaseEntity]:
        return [entity for entity in self.entities if entity.in_cluster]

    def to_dict(self) -> dict:
        return {
            "entities": [entity.to_dict() for entity in self.entities],
            "last_id": self.last_id
        }

    @staticmethod
    def from_dict(
            data: dict, keyed_vectors: gensim.models.keyedvectors.KeyedVectors) -> IEntityRepository:
        entities = [cast(BaseEntity, BaseEntity.from_dict(entity_data))
                    for entity_data in data["entities"]]
        return BaseEntityRepository(
            entities=entities, last_id=data["last_id"],
            keyed_vectors=keyed_vectors)
