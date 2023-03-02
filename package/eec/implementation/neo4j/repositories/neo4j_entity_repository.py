from eec.core.abstract.entity_repository import IEntityRepository
from eec.core.data_model import EntityModel
from eec.core.exceptions import NotFoundException, ArgumentException
from eec.implementation.neo4j.services.neo4j_service.neo4j_helper import Neo4JHelper
from eec.implementation.neo4j.services.neo4j_service.query_helpers.entity_helpers import *

import gensim
import numpy as np
from typing import Optional, cast

import logging


class Neo4JEntityRepository(IEntityRepository):
    def __init__(self,
                 keyed_vectors: gensim.models.Word2Vec):
        super().__init__()
        self.keyed_vectors = keyed_vectors
        self.neo4j_helper = Neo4JHelper.get_instance()
        self.logger = logging.getLogger(__name__)

    def get_entity_by_id(self, entity_id: str) -> EntityModel:
        result = self.neo4j_helper.run_query(
            Neo4J_GetEntityByIdHelper(entity_id))
        if result['entity'] is None:
            raise NotFoundException(f"Entity with id {entity_id} not found")
        return cast(EntityModel, result['entity'])

    def get_entity_by_mention(self, mention: str) -> EntityModel:
        result = self.neo4j_helper.run_query(
            Neo4J_GetEntityByMentionHelper(mention))
        if result['entity'] is None:
            raise NotFoundException(f"Entity with mention {mention} not found")
        return cast(EntityModel, result['entity'])

    def get_entities_by_source(self, source: str) -> list[EntityModel]:
        result = self.neo4j_helper.run_query(
            Neo4J_GetEntitiesBySourceHelper(source))
        if result['entities'] is None:
            raise NotFoundException(f"Entities with source {source} not found")
        return cast(list[EntityModel], result['entities'])

    def get_entity_by_source_id(self, source: str, source_id: str) -> EntityModel:
        result = self.neo4j_helper.run_query(
            Neo4J_GetEntityBySourceIdHelper(source, source_id))
        if result['entity'] is None:
            raise NotFoundException(
                f"Entity with source {source} and source id {source_id} not found")
        return cast(EntityModel, result['entity'])

    def get_all_entities(self) -> list[EntityModel]:
        result = self.neo4j_helper.run_query(Neo4J_GetAllEntitiesHelper())
        return cast(list[EntityModel], result['entities'])

    def add_entity(self, entity: EntityModel) -> EntityModel:
        self.calculate_entity_vector(entity)
        result = self.neo4j_helper.run_query(Neo4J_CreateEntityHelper(entity))
        return cast(EntityModel, result['entity'])

    def add_entities(self, entities: list[EntityModel]):
        for entity in entities:
            self.calculate_entity_vector(entity)
        result = self.neo4j_helper.run_query(Neo4J_CreateEntitiesHelper(entities))
        return cast(list[EntityModel], result['entities'])

    def delete_entity(self, entity_id: str) -> EntityModel:
        result = self.neo4j_helper.run_query(
            Neo4J_DeleteEntityByIdHelper(entity_id))
        if result['entity'] is None:
            raise NotFoundException(f"Entity with id {entity_id} not found")
        return cast(EntityModel, result['entity'])

    def delete_entities(self, entity_ids: list[str]):
        self.neo4j_helper.run_query(Neo4J_DeleteEntitiesByIdHelper(entity_ids))

    def is_in_repository(
            self, entity_id: Optional[str] = None, entity: Optional[EntityModel] = None,
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
        self.neo4j_helper.run_query(Neo4J_DeleteAllEntitiesHelper())

    def update_entity(self, entity: EntityModel) -> EntityModel:
        self.calculate_entity_vector(entity)
        result = self.neo4j_helper.run_query(Neo4J_UpdateEntityHelper(entity))
        if result['entity'] is None:
            raise NotFoundException(f"Entity with id {entity.entity_id} not found")
        return cast(EntityModel, result['entity'])

    def update_entities(self, entities: list[EntityModel]):
        for entity in entities:
            self.calculate_entity_vector(entity)
        self.neo4j_helper.run_query(Neo4J_UpdateEntitiesHelper(entities))

    def get_random_unlabeled_entity(self) -> EntityModel:
        result = self.neo4j_helper.run_query(Neo4J_GetRandomUnclusteredEntityHelper())
        if result['entity'] is None:
            raise NotFoundException("No unlabeled entities found")
        return cast(EntityModel, result['entity'])

    def get_random_unlabeled_entities(self, count: int) -> list[EntityModel]:
        result = self.neo4j_helper.run_query(Neo4J_GetRandomUnclusteredEntitiesHelper(count))
        if result['entities'] is None:
            raise NotFoundException("No unlabeled entities found")
        return cast(list[EntityModel], result['entities'])

    def calculate_entity_vector(self, entity: EntityModel):
        vecs = [
            self.keyed_vectors.wv[word] for word in entity.mention.split()
            if word in self.keyed_vectors.wv.key_to_index]
        if len(vecs) == 0:
            entity.has_mention_vector = False
            entity.mention_vector = np.zeros(
                self.keyed_vectors.vector_size, dtype=np.float32).tolist()
            return

        entity.has_mention_vector = True
        entity.mention_vector = np.mean(vecs, axis=0)

    def calculate_all_entity_vectors(self):
        entities = self.get_all_entities()
        for entity in entities:
            self.calculate_entity_vector(entity)
        self.update_entities(entities)

    def get_all_entities_in_cluster(self,) -> list[EntityModel]:
        result = self.neo4j_helper.run_query(Neo4J_GetAllEntitiesInClusterHelper())
        return cast(list[EntityModel], result['entities'])

    def to_dict(self) -> dict:
        return {
            "entities": [entity.to_dict() for entity in self.get_all_entities()],
        }
