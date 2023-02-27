from eec.interfaces.interface_user_repository.i_user_repository import IUserRepository
from eec.implementations.base.models.base_user import BaseUser
from eec.exceptions.general.exceptions import *


class BaseUserRepository(IUserRepository):

    def __init__(self, users: list[BaseUser] = [], last_id: int = 0):
        self.users = {
            user.get_user_id(): user for user in users
        }
        self.user_names = {
            user.get_user_name(): user for user in users
        }
        self.last_id = last_id

    def get_user_by_id(self, user_id: str) -> BaseUser:
        """Returns a user object by id"""
        if user_id in self.users:
            return self.users[user_id]
        raise NotFoundException(
            f'User with id {user_id} not found in repository')

    def get_user_by_name(self, user_name: str) -> BaseUser:
        """Returns a user object by name"""
        if user_name in self.user_names:
            return self.user_names[user_name]
        raise NotFoundException(
            f'User with name {user_name} not found in repository')

    def user_exists(self, user_id: str) -> bool:
        """Returns True if a user exists in the repository"""
        return user_id in self.users

    def user_name_exists(self, user_name: str) -> bool:
        return user_name in self.user_names

    def get_all_users(self) -> list[BaseUser]:
        """Returns a list of all user objects"""
        return list(self.users.values())

    def add_user(self, user: BaseUser) -> BaseUser:
        """Adds a user object to the repository"""
        if self.user_name_exists(user.get_user_name()):
            raise AlreadyExistsException(
                f'User with name {user.get_user_name()} already exists in repository')

        user.user_id = str(self.last_id)
        self.last_id += 1
        self.users[user.get_user_id()] = user
        self.user_names[user.get_user_name()] = user
        return user

    def change_username(self, user_id: str, user_name: str) -> BaseUser:
        if not self.user_exists(user_id):
            raise NotFoundException(
                f'User with id {user_id} not found in repository')

        if self.user_name_exists(user_name):
            raise AlreadyExistsException(
                f'User with name {user_name} already exists in repository')

        self.users[user_id].user_name = user_name

        for user_name in self.user_names:
            if self.user_names[user_name].get_user_id() == user_id:
                del self.user_names[user_name]
                self.user_names[user_name] = self.users[user_id]
                break

        return self.users[user_id]

    def change_role(self, user_id: str, role: str) -> BaseUser:
        if not self.user_exists(user_id):
            raise NotFoundException(
                f'User with id {user_id} not found in repository')
        self.users[user_id].role = role
        return self.users[user_id]

    def change_password(self, user_id: str, salt: str, hashed_password: str) -> BaseUser:
        """Updates a user object in the repository"""
        if not self.user_exists(user_id):
            raise NotFoundException(
                f'User with id {user_id} not found in repository')
        self.users[user_id].salt = salt
        self.users[user_id].hashed_password = hashed_password
        return self.users[user_id]

    def delete_user(self, user_id: str) -> bool:
        """Deletes a user object from the repository"""
        if not self.user_exists(user_id):
            raise NotFoundException(
                f'User with id {user_id} not found in repository')
        user = self.users[user_id]
        del self.users[user_id]
        del self.user_names[user.get_user_name()]
        return True

    def get_user_count(self) -> int:
        """Returns the number of users in the repository"""
        return len(self.users)

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the user repository object"""
        return {
            'users': [user.to_dict() for user in self.users.values()],
            'last_id': self.last_id
        }

    @classmethod
    def from_dict(cls, user_repository_dict: dict) -> 'BaseUserRepository':
        """Returns a user repository object from a dictionary"""
        users = [
            BaseUser.from_dict(user_dict)
            for user_dict in user_repository_dict['users']
        ]
        return cls(users, user_repository_dict['last_id'])
