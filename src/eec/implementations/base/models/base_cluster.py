from eec.interfaces.interface_cluster.i_cluster import ICluster
from eec.implementations.base.models.base_entity import BaseEntity
from eec.implementations.base.repositories.base_entity_repository import BaseEntityRepository
from eec.exceptions.general.exceptions import *

import numpy as np
from typing import Optional, Callable


class BaseCluster(ICluster):

    def __init__(self, cluster_id: str,
                 cluster_name: str,
                 entities: list[BaseEntity],
                 cluster_vector: np.ndarray = np.array([])):
        super().__init__(cluster_id, cluster_name)
        self.cluster_name = cluster_name
        self.entities: list[BaseEntity] = entities
        self.cluster_vector: np.ndarray = cluster_vector
        if self.cluster_vector.size == 0:
            self.calculate_cluster_vector()

    def get_entities(self) -> list[BaseEntity]:
        '''Returns the entities of the cluster.'''
        return self.entities

    def get_entity_by_id(self, entity_id: str) -> BaseEntity:
        '''Returns the entity with the given entity id.'''
        for entity in self.entities:
            if entity.get_entity_id() == entity_id:
                return entity
        raise NotFoundException(
            f"Entity with id {entity_id} not found in cluster {self.cluster_id}-{self.cluster_name}")

    def get_entity_by_mention(
            self, mention: str) -> BaseEntity:
        '''Returns the entity with the given mention.'''
        for entity in self.entities:
            if entity.get_mention() == mention:
                return entity
        raise NotFoundException(
            f"Entity with mention {mention} not found in cluster {self.cluster_id}-{self.cluster_name}")

    def get_entity_by_source_id(
            self, source: str, source_id: str) -> BaseEntity:
        '''Returns the entity with the given source and source id.'''
        for entity in self.entities:
            if entity.get_entity_source() == source and entity.get_entity_source_id() == source_id:
                return entity
        raise NotFoundException(
            f"Entity with source {source} and source_id {source_id} not found in cluster {self.cluster_id}-{self.cluster_name}")

    def get_entities_by_source(
            self, source: str) -> list[BaseEntity]:
        '''Returns the entities with the given source.'''
        entities = []
        for entity in self.entities:
            if entity.get_entity_source() == source:
                entities.append(entity)
        return entities

    def is_in_cluster(self, entity_id: Optional[str] = None,
                      entity_source: Optional[str] = None,
                      entity_source_id: Optional[str] = None,
                      entity: Optional[BaseEntity] = None) -> bool:
        '''
        Returns True if the entity is in the cluster, False otherwise.
        You must provide at least one of the following: entity_id, entity or both entity_source and entity_source_id
        '''
        try:
            if entity is not None:
                return entity in self.entities

            if entity_id is not None:
                return self.get_entity_by_id(entity_id) is not None

            if entity_source is not None and entity_source_id is not None:
                return self.get_entity_by_source_id(entity_source, entity_source_id) is not None

        except NotFoundException:
            return False

        if (entity_source is None and entity_source_id is not None) or (entity_source is not None and entity_source_id is None):
            raise ArgumentException("You must provide both entity_source and entity_source_id")

        raise ArgumentException(
            "You must provide at least one of the following: entity_id, entity or both entity_source and entity_source_id")

    def add_entity(self, entity: BaseEntity):
        '''Adds the given entity to the cluster.'''
        if self.is_in_cluster(entity=entity):
            raise AlreadyExistsException(
                f"Entity with id {entity.get_entity_id()} and name {entity.get_mention()} is already in the cluster {self.cluster_id}-{self.cluster_name}")
        if entity.in_cluster:
            raise AlreadyInClusterException(
                f"Entity with id {entity.get_entity_id()} and name {entity.get_mention()} is in cluster with id {entity.cluster_id}")
        self.entities.append(entity)
        self.calculate_cluster_vector()

    def remove_entity(
            self, entity_id: Optional[str] = None, entity_source: Optional[str] = None,
            entity_source_id: Optional[str] = None, entity: Optional[BaseEntity] = None) -> BaseEntity:
        '''
        Removes the given entity from the cluster.
        You must provide at least one of the following: entity_id, entity or both entity_source and entity_source_id
        '''
        if entity is not None:
            self.entities.remove(entity)
            self.calculate_cluster_vector()
            return entity

        if entity_id is not None:
            entity = self.get_entity_by_id(entity_id)
            self.entities.remove(self.get_entity_by_id(entity_id))
            self.calculate_cluster_vector()
            return entity

        if entity_source is not None and entity_source_id is not None:
            entity = self.get_entity_by_source_id(entity_source, entity_source_id)
            self.entities.remove(
                entity)
            self.calculate_cluster_vector()
            return entity

        elif (entity_source is None and entity_source_id is not None) or (entity_source is not None and entity_source_id is None):
            raise ArgumentException("You must provide both entity_source and entity_source_id")

        raise ArgumentException(
            "You must provide at least one of the following: entity_id, entity or both entity_source and entity_source_id")

    def calculate_cluster_vector(self, ):
        '''Calculates the cluster vector based on the entities in the cluster.'''
        self.cluster_vector = np.mean(
            [entity.get_mention_vector() for entity in self.entities], axis=0)

    def get_closest_entities(
            self, entity: BaseEntity,
            distance_function: Callable[[np.ndarray, np.ndarray],
                                        np.ndarray],
            top_n: int = 10,) -> list[BaseEntity]:
        '''Returns the top_n closest entities to the given entity.'''
        _all_entity_vectors = np.array([entity.get_mention_vector() for entity in self.entities])
        similarities = distance_function(_all_entity_vectors, entity.get_mention_vector())
        return [self.entities[i] for i in np.argpartition(similarities, -top_n)[-top_n:]]

    def to_dict(self) -> dict:
        '''Returns a dict representation of the cluster.'''
        return {
            "cluster_id": self.cluster_id,
            "cluster_name": self.cluster_name,
            "entities": [entity.entity_id for entity in self.entities],
            "cluster_vector": self.cluster_vector.tolist()
        }

    @staticmethod
    def from_dict(cluster_dict: dict, entity_repository: BaseEntityRepository) -> ICluster:
        '''Returns a cluster from a dict representation.'''
        return BaseCluster(cluster_dict["cluster_id"],
                           cluster_dict["cluster_name"],
                           [entity_repository.get_entity_by_id(entity_id)
                            for entity_id in cluster_dict["entities"]],
                           np.array(cluster_dict["cluster_vector"]))

    def __str__(self):
        return f"Cluster {self.cluster_id}-{self.cluster_name}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.cluster_id == other.cluster_id

    def __hash__(self):
        return hash(self.cluster_id)
