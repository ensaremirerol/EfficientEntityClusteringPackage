from eec.core.abstract.user_repository import IUserRepository
from eec.core.data_model.user_model import UserModel
from eec.core.exceptions.exceptions import NotFoundException, AlreadyExistsException


class BaseUserRepository(IUserRepository):

    def __init__(self, users: list[UserModel] = [], last_id: int = 0):
        self.users = {
            user.user_id: user for user in users
        }
        self.usernames = {
            user.username: user for user in users
        }
        self.last_id = last_id

    def get_user_by_id(self, user_id: str) -> UserModel:
        """Returns a user object by id"""
        if user_id in self.users:
            return self.users[user_id]
        raise NotFoundException(
            f'User with id {user_id} not found in repository')

    def get_user_by_name(self, username: str) -> UserModel:
        """Returns a user object by name"""
        if username in self.usernames:
            return self.usernames[username]
        raise NotFoundException(
            f'User with name {username} not found in repository')

    def user_exists(self, user_id: str) -> bool:
        """Returns True if a user exists in the repository"""
        return user_id in self.users

    def username_exists(self, username: str) -> bool:
        return username in self.usernames

    def get_all_users(self) -> list[UserModel]:
        """Returns a list of all user objects"""
        return list(self.users.values())

    def add_user(self, username: str, hashed_password: str, role: str = ''):
        """Adds a user object to the repository"""
        if self.username_exists(username):
            raise AlreadyExistsException(
                f'User with name {username} already exists in repository')

        user = UserModel(username, hashed_password, role)

        user.user_id = str(self.last_id)
        self.last_id += 1
        self.users[user.user_id] = user
        self.usernames[user.username] = user
        return user

    def change_username(self, user_id: str, username: str) -> UserModel:
        if not self.user_exists(user_id):
            raise NotFoundException(
                f'User with id {user_id} not found in repository')

        if self.username_exists(username):
            raise AlreadyExistsException(
                f'User with name {username} already exists in repository')

        self.users[user_id].username = username

        for username in self.usernames:
            if self.usernames[username].user_id == user_id:
                del self.usernames[username]
                self.usernames[username] = self.users[user_id]
                break

        return self.users[user_id]

    def change_role(self, user_id: str, role: str) -> UserModel:
        if not self.user_exists(user_id):
            raise NotFoundException(
                f'User with id {user_id} not found in repository')
        self.users[user_id].role = role
        return self.users[user_id]

    def change_password(self, user_id: str, hashed_password: str) -> UserModel:
        """Updates a user object in the repository"""
        if not self.user_exists(user_id):
            raise NotFoundException(
                f'User with id {user_id} not found in repository')
        self.users[user_id].hashed_password = hashed_password
        return self.users[user_id]

    def delete_user(self, user_id: str) -> bool:
        """Deletes a user object from the repository"""
        if not self.user_exists(user_id):
            raise NotFoundException(
                f'User with id {user_id} not found in repository')
        user = self.users[user_id]
        del self.users[user_id]
        del self.usernames[user.username]
        return True

    def get_user_count(self) -> int:
        """Returns the number of users in the repository"""
        return len(self.users)

    def to_dict(self, include_passwords=False) -> dict:
        """Returns a dictionary representation of the user repository object"""
        return {
            'users': [user.to_dict(include_password=include_passwords) for user in self.users.values()],
            'last_id': self.last_id
        }

    @classmethod
    def from_dict(cls, user_repository_dict: dict) -> 'BaseUserRepository':
        """Returns a user repository object from a dictionary"""
        users = [
            UserModel.from_dict(user_dict)
            for user_dict in user_repository_dict['users']
        ]
        return cls(users, user_repository_dict['last_id'])

    def encode(self) -> dict:
        return self.to_dict(include_passwords=True)

    @classmethod
    def decode(cls, user_repository_dict: dict) -> 'BaseUserRepository':
        return cls.from_dict(user_repository_dict)
