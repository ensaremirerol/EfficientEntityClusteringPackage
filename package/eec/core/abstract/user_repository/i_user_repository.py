from abc import ABC, abstractmethod
from eec.core.data_model import UserModel


class IUserRepository(ABC):
    """Interface for user repository class"""

    def __init__(self):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> UserModel:
        """Returns a user object by id"""
        pass

    @abstractmethod
    def get_user_by_name(self, username: str) -> UserModel:
        """Returns a user object by name"""
        pass

    @abstractmethod
    def user_exists(self, user_id: str) -> bool:
        """Returns True if a user exists in the repository"""
        pass

    @abstractmethod
    def username_exists(self, username: str) -> bool:
        """Returns True if a user name exists in the repository"""
        pass

    @abstractmethod
    def get_all_users(self) -> list[UserModel]:
        """Returns a list of all user objects"""
        pass

    @abstractmethod
    def add_user(self, username: str, hashed_password: str, role: str) -> UserModel:
        """Adds a user object to the repository"""
        pass

    @abstractmethod
    def change_username(self, user_id: str, username: str, role: str = '') -> UserModel:
        """Updates a user object in the repository"""
        pass

    @abstractmethod
    def change_role(self, user_id: str, role: str) -> UserModel:
        """Updates a user object in the repository"""
        pass

    @abstractmethod
    def change_password(self, user_id: str, hashed_password: str) -> UserModel:
        """Updates a user object in the repository"""
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> bool:
        """Deletes a user object from the repository"""
        pass

    @abstractmethod
    def get_user_count(self) -> int:
        """Returns the number of users in the repository"""
        pass

    @abstractmethod
    def to_dict(self, include_passwords=False) -> dict:
        """Returns a dictionary representation of the user repository object"""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, user_repository_dict: dict) -> 'IUserRepository':
        """Returns a user repository object from a dictionary"""
        pass
