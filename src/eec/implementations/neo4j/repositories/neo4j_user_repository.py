from eec.interfaces.interface_user_repository.i_user_repository import IUserRepository
from eec.implementations.neo4j.models.neo4j_user import Neo4JUser
from eec.exceptions.general.exceptions import *
from eec.implementations.neo4j.neo4j_services.neo4j_helper import Neo4JHelper
from eec.implementations.neo4j.neo4j_services.query_helpers.user_helpers import *
from eec.implementations.neo4j.exceptions.neo4j_exceptions import *
from typing import cast


class Neo4JUserRepository(IUserRepository):

    def __init__(self):
        self.neo4j_helper = Neo4JHelper.get_instance()

    def get_user_by_id(self, user_id: str) -> Neo4JUser:
        """Returns a user object by id"""
        result = self.neo4j_helper.run_query(
            Neo4J_GetUserByIdHelper(user_id))

        if result['user'] is None:
            raise NotFoundException(f'User with id {user_id} not found in repository')
        return cast(Neo4JUser, result['user'])

    def get_user_by_name(self, user_name: str) -> Neo4JUser:
        """Returns a user object by name"""
        result = self.neo4j_helper.run_query(
            Neo4J_GetUserByUsernameHelper(user_name))

        if result['user'] is None:
            raise NotFoundException(
                f'User with name {user_name} not found in repository')
        return cast(Neo4JUser, result['user'])

    def user_exists(self, user_id: str) -> bool:
        """Returns True if a user exists in the repository"""
        reuslt = self.neo4j_helper.run_query(
            Neo4J_GetUserByIdHelper(user_id))
        return reuslt['user'] is not None

    def user_name_exists(self, user_name: str) -> bool:
        return self.neo4j_helper.run_query(
            Neo4J_GetUserByUsernameHelper(user_name))['user'] is not None

    def get_all_users(self) -> list[Neo4JUser]:
        """Returns a list of all user objects"""
        result = self.neo4j_helper.run_query(Neo4J_GetAllUsersHelper())
        return cast(list[Neo4JUser], result['users'])

    def add_user(self, username: str, hashed_password: str, role: str='') -> Neo4JUser:
        """Adds a user object to the repository"""
        if self.user_name_exists(username):
            raise AlreadyExistsException(
                f'User with name {username} already exists in repository')
        user = Neo4JUser(username, hashed_password, role)
        result = self.neo4j_helper.run_query(
            Neo4J_CreateUserHelper(user))

        if result['user'] is None:
            raise Exception('Failed to create user')
        return cast(Neo4JUser, result['user'])

    def change_username(self, user_id: str, user_name:str) -> Neo4JUser:
        if not self.user_exists(user_id):
            raise NotFoundException(
                f'User with id {user_id} not found in repository')

        if self.user_name_exists(user_name):
            raise AlreadyExistsException(
                f'User with name {user_name} already exists in repository')

        result = self.neo4j_helper.run_query(
            Neo4J_ChangeUsernameHelper(user_id, user_name))

        if result['user'] is None:
            raise Exception('Failed to update user')
        return cast(Neo4JUser, result['user'])
    
    def change_role(self, user_id: str, role: str) -> Neo4JUser:
        if not self.user_exists(user_id):
            raise NotFoundException(
                f'User with id {user_id} not found in repository')

        result = self.neo4j_helper.run_query(
            Neo4J_ChangeUserRoleHelper(user_id, role))

        if result['user'] is None:
            raise Exception('Failed to update user')
        return cast(Neo4JUser, result['user'])

    def change_password(self, user_id: str, hashed_password: str) -> Neo4JUser:
        """Updates a user object in the repository"""
        if not self.user_exists(user_id):
            raise NotFoundException(
                f'User with id {user_id} not found in repository')
        result = self.neo4j_helper.run_query(
            Neo4J_ChangeUserPasswordHelper(user_id, hashed_password))

        if result['user'] is None:
            raise Exception('Failed to change password')
        return cast(Neo4JUser, result['user'])

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
    