from core.abstract.entity_repository import IEntityRepository
from core.data_model import EntityModel
from core.exceptions import *

import gensim
import numpy as np
from typing import Optional, cast

import logging


class BaseEntityRepository(IEntityRepository):
    def __init__(self,
                 entities: list[EntityModel],
                 last_id: int,
                 keyed_vectors: gensim.models.Word2Vec):
        super().__init__()
        self.keyed_vectors = keyed_vectors
        self.entities: list[EntityModel] = entities
        self._entity_id_to_index = {entity.entity_id: i for i, entity in enumerate(entities)}
        self.last_id = last_id
        self.logger = logging.getLogger(__name__)

    def get_entity_by_id(self, entity_id: str) -> EntityModel:
        if entity_id in self._entity_id_to_index:
            return self.entities[self._entity_id_to_index[entity_id]]
        raise NotFoundException(f"Entity with id {entity_id} not found")

    def get_entities_by_source(self, source: str) -> list[EntityModel]:
        return [entity for entity in self.entities if entity.entity_source == source]

    def get_entity_by_source_id(self, source: str, source_id: str) -> EntityModel:
        for entity in self.entities:
            if entity.entity_source == source and entity.entity_source_id == source_id:
                return entity
        raise NotFoundException(f"Entity with source {source} and source_id {source_id} not found")

    def get_all_entities(self) -> list[EntityModel]:
        return [entity for entity in self.entities]

    def add_entity(self, entity: EntityModel) -> EntityModel:
        if self.is_in_repository(
                entity_source=entity.entity_source, entity_source_id=entity.entity_source_id):
            raise AlreadyExistsException(
                f"Entity with source {entity.entity_source} and source_id {entity.entity_source_id} already exists")
        self.calculate_entity_vector(entity)
        self.last_id += 1
        entity.entity_id = str(self.last_id)
        self.entities.append(entity)
        return entity

    def add_entities(self, entities: list[EntityModel], suppress_exceptions=False):
        _entities = []
        for entity in entities:
            if self.is_in_repository(
                    entity_source=entity.entity_source, entity_source_id=entity.entity_source_id):
                if not suppress_exceptions:
                    raise AlreadyExistsException(
                        f"Entity with source {entity.entity_source} and source_id {entity.entity_source_id} already exists")
                self.logger.warning(
                    f"Entity with source {entity.entity_source} and source_id {entity.entity_source_id} already exists\n"
                    "Skipping entity {entity.mention}")

        for entity in entities:
            try:
                _entities.append(self.add_entity(entity))
            except AlreadyExistsException as e:
                continue
        return _entities

    def delete_entity(self, entity_id: str) -> EntityModel:
        if entity_id in self._entity_id_to_index:
            index = self._entity_id_to_index[entity_id]
            copy_entity = EntityModel.from_dict(self.entities[index].to_dict())
            del self.entities[index]
            self._entity_id_to_index = {entity.entity_id: i for i,
                                        entity in enumerate(self.entities)}
            return copy_entity
        raise NotFoundException(f"Entity with id {entity_id} not found")

    def delete_entities(self, entity_ids: list[str], suppress_exceptions=False):
        for entity_id in entity_ids:
            if not self.is_in_repository(entity_id=entity_id):
                if not suppress_exceptions:
                    raise NotFoundException(f"Entity with id {entity_id} not found")
                self.logger.warning(
                    f"Entity with id {entity_id} not found\nSkipping entity {entity_id}")
        _entities = []
        for entity_id in entity_ids:
            try:
                _entities.append(self.delete_entity(entity_id))
            except NotFoundException as e:
                continue

    def is_in_repository(
            self, entity_id: Optional[str] = None, entity: Optional[EntityModel] = None,
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

    def get_random_unlabeled_entity(self) -> EntityModel:
        unlabeled_entities = []
        unlabeled_entities = [entity for entity in self.entities if not entity.has_cluster]
        if len(unlabeled_entities) == 0:
            raise NotFoundException("No unlabeled entities found")
        return unlabeled_entities[np.random.randint(0, len(unlabeled_entities))]

    def get_random_unlabeled_entities(self, count: int) -> list[EntityModel]:
        unlabeled_entities = []
        unlabeled_entities = [entity for entity in self.entities if not entity.has_cluster]
        if len(unlabeled_entities) == 0:
            raise NotFoundException("No unlabeled entities found")
        if len(unlabeled_entities) < count:
            return unlabeled_entities
        indexes = np.random.randint(0, len(unlabeled_entities), count)
        return [unlabeled_entities[index] for index in indexes]

    def calculate_entity_vector(self, entity: EntityModel):
        processed_mention = entity.mention.lower()
        processed_mention = gensim.utils.simple_preprocess(processed_mention)
        vecs = [
            self.keyed_vectors.wv[word] for word in processed_mention
            if word in self.keyed_vectors.wv.key_to_index]
        if len(vecs) == 0:
            entity.has_mention_vector = False
            entity.mention_vector = []
            return

        entity.has_mention_vector = True
        entity.mention_vector = np.mean(vecs, axis=0).tolist()

    def calculate_all_entity_vectors(self):
        for entity in self.entities:
            self.calculate_entity_vector(entity)

    def get_all_entities_in_cluster(self,) -> list[EntityModel]:
        return [entity for entity in self.entities if entity.has_cluster]

    def to_dict(self) -> dict:
        return {
            "entities": [entity.to_dict() for entity in self.entities],
            "last_id": self.last_id
        }

    @classmethod
    def from_dict(cls,
                  data: dict, keyed_vectors: gensim.models.Word2Vec) -> 'BaseEntityRepository':
        entities = [cast(EntityModel, EntityModel.from_dict(entity_data))
                    for entity_data in data["entities"]]
        return BaseEntityRepository(
            entities=entities, last_id=data["last_id"],
            keyed_vectors=keyed_vectors)

    def encode(self):
        return self.to_dict()

    @classmethod
    def decode(cls, data, keyed_vectors):
        return cls.from_dict(data, keyed_vectors)
