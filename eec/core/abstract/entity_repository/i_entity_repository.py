from core.data_model import EntityModel

from typing import Optional
from abc import ABC, abstractmethod


class IEntityRepository(ABC):
    """
    Interface for an entity repository.
    """
    @abstractmethod
    def get_entity_by_id(self, entity_id: str) -> EntityModel:
        '''Returns the entity with the given entity id.'''
        pass

    @abstractmethod
    def get_entities_by_source(self, source: str) -> list[EntityModel]:
        '''Returns the entities with the given source.'''
        pass

    @abstractmethod
    def get_entity_by_source_id(self, source: str, source_id: str) -> EntityModel:
        '''Returns the entities with the given source and source id.'''
        pass

    @abstractmethod
    def get_all_entities(self) -> list[EntityModel]:
        '''Returns all entities.'''
        pass

    @abstractmethod
    def get_all_entities_in_cluster(self, cluster_id: str) -> list[EntityModel]:
        '''Returns all entities in the given cluster.'''
        pass

    @abstractmethod
    def add_entity(self, entity: EntityModel) -> EntityModel:
        '''Adds the given entity.'''
        pass

    @abstractmethod
    def add_entities(self, entities: list[EntityModel], suppress_exceptions=False) -> list[EntityModel]:
        '''Adds the given entities.'''
        pass

    @abstractmethod
    def delete_entity(self, entity_id: str) -> EntityModel:
        '''Deletes the given entity.'''
        pass

    @abstractmethod
    def delete_entities(self, entity_ids: list[str], suppress_exceptions=False) -> list[EntityModel]:
        '''Deletes the given entities.'''
        pass

    @abstractmethod
    def is_in_repository(
            self, entity_id: Optional[str] = None, entity: Optional[EntityModel] = None,
            entity_source: Optional[str] = None, entity_source_id: Optional[str] = None) -> bool:
        '''
        Returns whether the given entity is in the repository.
        You must provide at least one of the following: entity_id, entity or both entity_source and entity_source_id
        '''
        pass

    @abstractmethod
    def delete_all_entities(self):
        '''Deletes all entities.'''
        pass

    @abstractmethod
    def get_random_unlabeled_entity(self) -> EntityModel:
        '''Returns a random unlabeled entity.'''
        pass

    @abstractmethod
    def get_random_unlabeled_entities(self, count: int) -> list[EntityModel]:
        '''Returns a list of random unlabeled entities.'''
        pass
