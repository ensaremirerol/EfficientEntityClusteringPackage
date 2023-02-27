from abc import ABC, abstractmethod
from eec.interfaces.interface_user.i_user import IUser


class IUserRepository(ABC):
    """Interface for user repository class"""

    def __init__(self):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> IUser:
        """Returns a user object by id"""
        pass

    @abstractmethod
    def get_user_by_name(self, user_name: str) -> IUser:
        """Returns a user object by name"""
        pass

    @abstractmethod
    def user_exists(self, user_id: str) -> bool:
        """Returns True if a user exists in the repository"""
        pass

    @abstractmethod
    def user_name_exists(self, user_name: str) -> bool:
        """Returns True if a user name exists in the repository"""
        pass

    @abstractmethod
    def get_all_users(self) -> list[IUser]:
        """Returns a list of all user objects"""
        pass

    @abstractmethod
    def add_user(self, user: IUser) -> IUser:
        """Adds a user object to the repository"""
        pass

    @abstractmethod
    def change_username(self, user_id: str, username: str) -> IUser:
        """Updates a user object in the repository"""
        pass

    @abstractmethod
    def change_role(self, user_id: str, role: str) -> IUser:
        """Updates a user object in the repository"""
        pass

    @abstractmethod
    def change_password(self, user_id: str, hashed_password: str) -> IUser:
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
    def to_dict(self) -> dict:
        """Returns a dictionary representation of the user repository object"""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, user_repository_dict: dict) -> 'IUserRepository':
        """Returns a user repository object from a dictionary"""
        pass
