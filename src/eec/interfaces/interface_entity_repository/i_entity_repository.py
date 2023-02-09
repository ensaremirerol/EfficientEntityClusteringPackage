from eec.interfaces.interface_entity.i_entity import IEntity

from typing import Optional
import abc


class IEntityRepository(abc.ABC):
    @abc.abstractmethod
    def get_entity_by_id(self, entity_id: str) -> IEntity:
        '''Returns the entity with the given entity id.'''
        pass

    @abc.abstractmethod
    def get_entity_by_mention(self, mention: str) -> IEntity:
        '''Returns the entity with the given mention.'''
        pass

    @abc.abstractmethod
    def get_entities_by_source(self, source: str) -> list[IEntity]:
        '''Returns the entities with the given source.'''
        pass

    @abc.abstractmethod
    def get_entity_by_source_id(self, source: str, source_id: str) -> IEntity:
        '''Returns the entities with the given source and source id.'''
        pass

    @abc.abstractmethod
    def get_all_entities(self) -> list[IEntity]:
        '''Returns all entities.'''
        pass

    @abc.abstractmethod
    def get_all_entities_in_cluster(self, cluster_id: str) -> list[IEntity]:
        '''Returns all entities in the given cluster.'''
        pass

    @abc.abstractmethod
    def update_entity(self, entity: IEntity):
        '''Updates the given entity.'''
        pass

    @abc.abstractmethod
    def add_entity(self, entity: IEntity) -> IEntity:
        '''Adds the given entity.'''
        pass

    @abc.abstractmethod
    def add_entities(self, entities: list[IEntity]) -> list[IEntity]:
        '''Adds the given entities.'''
        pass

    @abc.abstractmethod
    def delete_entity(self, entity_id: str):
        '''Deletes the given entity.'''
        pass

    @abc.abstractmethod
    def delete_entities(self, entity_ids: list[str]):
        '''Deletes the given entities.'''
        pass

    @abc.abstractmethod
    def is_in_repository(
            self, entity_id: Optional[str] = None, entity: Optional[IEntity] = None,
            entity_source: Optional[str] = None, entity_source_id: Optional[str] = None) -> bool:
        '''
        Returns whether the given entity is in the repository.
        You must provide at least one of the following: entity_id, entity or both entity_source and entity_source_id
        '''
        pass

    @abc.abstractmethod
    def delete_all_entities(self):
        '''Deletes all entities.'''
        pass

    @abc.abstractmethod
    def get_random_unlabeled_entity(self) -> IEntity:
        '''Returns a random unlabeled entity.'''
        pass

    @abc.abstractmethod
    def get_random_unlabeled_entities(self, count: int) -> list[IEntity]:
        '''Returns a list of random unlabeled entities.'''
        pass
