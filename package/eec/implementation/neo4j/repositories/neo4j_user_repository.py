from eec.core.abstract.user_repository import IUserRepository
from eec.core.data_model import UserModel
from eec.core.exceptions import NotFoundException, AlreadyExistsException
from eec.implementation.neo4j.services.neo4j_service.neo4j_helper import Neo4JHelper
from eec.implementation.neo4j.services.neo4j_service.query_helpers.user_helpers import *
from eec.implementation.neo4j.exceptions.neo4j_exceptions import Neo4J_DoNotUseThisException

from typing import cast


class Neo4JUserRepository(IUserRepository):

    def __init__(self):
        self.neo4j_helper = Neo4JHelper.get_instance()

    def get_user_by_id(self, user_id: str) -> UserModel:
        """Returns a user object by id"""
        result = self.neo4j_helper.run_query(
            Neo4J_GetUserByIdHelper(user_id))

        if result['user'] is None:
            raise NotFoundException(f'User with id {user_id} not found in repository')
        return cast(UserModel, result['user'])

    def get_user_by_name(self, username: str) -> UserModel:
        """Returns a user object by name"""
        result = self.neo4j_helper.run_query(
            Neo4J_GetUserByUsernameHelper(username))

        if result['user'] is None:
            raise NotFoundException(
                f'User with name {username} not found in repository')
        return cast(UserModel, result['user'])

    def user_exists(self, user_id: str) -> bool:
        """Returns True if a user exists in the repository"""
        reuslt = self.neo4j_helper.run_query(
            Neo4J_GetUserByIdHelper(user_id))
        return reuslt['user'] is not None

    def username_exists(self, username: str) -> bool:
        return self.neo4j_helper.run_query(
            Neo4J_GetUserByUsernameHelper(username))['user'] is not None

    def get_all_users(self) -> list[UserModel]:
        """Returns a list of all user objects"""
        result = self.neo4j_helper.run_query(Neo4J_GetAllUsersHelper())
        return cast(list[UserModel], result['users'])

    def add_user(self, username: str, hashed_password: str, role: str='') -> UserModel:
        """Adds a user object to the repository"""
        if self.username_exists(username):
            raise AlreadyExistsException(
                f'User with name {username} already exists in repository')
        user = UserModel(user_id='', username=username,
                         hashed_password=hashed_password, role=role)
        result = self.neo4j_helper.run_query(
            Neo4J_CreateUserHelper(user))

        if result['user'] is None:
            raise Exception('Failed to create user')
        return cast(UserModel, result['user'])

    def change_username(self, user_id: str, username:str) -> UserModel:
        if not self.user_exists(user_id):
            raise NotFoundException(
                f'User with id {user_id} not found in repository')

        if self.username_exists(username):
            raise AlreadyExistsException(
                f'User with name {username} already exists in repository')

        result = self.neo4j_helper.run_query(
            Neo4J_ChangeUsernameHelper(user_id, username))

        if result['user'] is None:
            raise Exception('Failed to update user')
        return cast(UserModel, result['user'])
    
    def change_role(self, user_id: str, role: str) -> UserModel:
        if not self.user_exists(user_id):
            raise NotFoundException(
                f'User with id {user_id} not found in repository')

        result = self.neo4j_helper.run_query(
            Neo4J_ChangeUserRoleHelper(user_id, role))

        if result['user'] is None:
            raise Exception('Failed to update user')
        return cast(UserModel, result['user'])

    def change_password(self, user_id: str, hashed_password: str) -> UserModel:
        """Updates a user object in the repository"""
        if not self.user_exists(user_id):
            raise NotFoundException(
                f'User with id {user_id} not found in repository')
        result = self.neo4j_helper.run_query(
            Neo4J_ChangeUserPasswordHelper(user_id, hashed_password))

        if result['user'] is None:
            raise Exception('Failed to change password')
        return cast(UserModel, result['user'])

    def delete_user(self, user_id: str) -> bool:
        """Deletes a user object from the repository"""
        if not self.user_exists(user_id):
            raise NotFoundException(
                f'User with id {user_id} not found in repository')
        result = self.neo4j_helper.run_query(
            Neo4J_DeleteUserHelper(user_id))
        
        if result['user'] is None:
            raise Exception('Failed to delete user')
        return True

    def get_user_count(self) -> int:
        """Returns the number of users in the repository"""
        return len(self.get_all_users())

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the user repository object"""
        return {
            'users': [user.to_dict() for user in self.get_all_users()],
        }

    @classmethod
    def from_dict(cls, user_repository_dict: dict) -> 'Neo4JUserRepository':
        """Returns a user repository object from a dictionary"""
        raise Neo4J_DoNotUseThisException(
            'Neo4JUserRepository.from_dict() is not implemented')
    