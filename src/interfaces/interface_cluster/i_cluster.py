from src.interfaces.interface_entity.i_entity import IEntity
from exceptions.general.exceptions import *

import abc
from typing import Optional


class ICluster(abc.ABC):
    def __init__(self, cluster_id: str,
                 cluster_name: str,):
        self.cluster_id = cluster_id
        self.cluster_name = cluster_name

    def get_cluster_id(self) -> str:
        '''Returns the cluster id of the cluster.'''
        return self.cluster_id

    def get_cluster_name(self) -> str:
        '''Returns the cluster name of the cluster.'''
        return self.cluster_name

    @abc.abstractmethod
    def get_entities(self) -> list[IEntity]:
        '''Returns the entities of the cluster.'''
        pass

    @abc.abstractmethod
    def get_entity_by_id(self, entity_id: str) -> IEntity:
        '''Returns the entity with the given entity id.'''
        pass

    @abc.abstractmethod
    def get_entity_by_mention(
            self, mention: str) -> IEntity:
        '''Returns the entity with the given mention.'''
        pass

    @abc.abstractmethod
    def get_entity_by_source_id(
            self, source: str, source_id: str) -> IEntity:
        '''Returns the entity with the given source and source id.'''
        pass

    @abc.abstractmethod
    def get_entities_by_source(
            self, source: str) -> list[IEntity]:
        '''Returns the entities with the given source.'''
        pass

    @abc.abstractmethod
    def is_in_cluster(self, entity_id: Optional[str] = None,
                      entity_source: Optional[str] = None,
                      entity_source_id: Optional[str] = None,
                      entity: Optional[IEntity] = None) -> bool:
        '''
        Returns True if the entity is in the cluster, False otherwise.
        You must provide at least one of the following: entity_id, entity or both entity_source and entity_source_id
        '''
        pass

    @abc.abstractmethod
    def add_entity(self, entity: IEntity):
        '''Adds the given entity to the cluster.'''
        pass

    @abc.abstractmethod
    def remove_entity(
            self, entity_id: Optional[str] = None, entity_source: Optional[str] = None,
            entity_source_id: Optional[str] = None, entity: Optional[IEntity] = None):
        '''
        Removes the given entity from the cluster.
        You must provide at least one of the following: entity_id, entity or both entity_source and entity_source_id
        '''
        pass

    def __eq__(self, other):
        if isinstance(other, ICluster):
            return self.cluster_id == other.cluster_id
        return False

    def __hash__(self):
        return hash((self.cluster_id))

    def __str__(self):
        return self.cluster_id + " " + self.cluster_name

    def __repr__(self):
        return self.__str__()
