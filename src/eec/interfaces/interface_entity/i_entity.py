import abc
from typing import Optional


class IEntity(abc.ABC):
    def __init__(
            self, mention: str, entity_id: str, entity_source: str, entity_source_id: str,
            in_cluster: bool = False, cluster_id: Optional[str] = None):
        self.mention = mention
        self.entity_id = entity_id
        self.entity_source = entity_source
        self.entity_source_id = entity_source_id
        self.in_cluster = in_cluster
        self.cluster_id = cluster_id

    def get_mention(self) -> str:
        '''Returns the mention of the entity.'''
        return self.mention

    def get_entity_id(self) -> str:
        '''Returns the entity id of the entity.'''
        return self.entity_id

    def get_entity_source(self) -> str:
        '''Returns the main entity source(which datasource) of the entity.'''
        return self.entity_source

    def get_entity_source_id(self) -> str:
        '''Returns the id of the entity in the main entity source(which datasource) of the entity.'''
        return self.entity_source_id

    def get_in_cluster(self) -> bool:
        '''Returns True if the entity is in a cluster, False otherwise.'''
        return self.in_cluster

    def get_cluster_id(self) -> Optional[str]:
        '''Returns the cluster id of the entity.'''
        return self.cluster_id

    @abc.abstractmethod
    def set_cluster_id(self, cluster_id: str):
        '''Sets the cluster id of the entity.'''
        pass

    def __eq__(self, other):
        if isinstance(other, IEntity):
            return self.mention == other.mention and self.entity_id == other.entity_id and self.entity_source == other.entity_source and self.entity_source_id == other.entity_source_id
        return False

    def __hash__(self):
        return hash((self.mention, self.entity_id, self.entity_source, self.entity_source_id))

    def __str__(self):
        return self.mention + " " + self.entity_id + " " + self.entity_source + " " + self.entity_source_id

    def __repr__(self):
        return self.__str__()
