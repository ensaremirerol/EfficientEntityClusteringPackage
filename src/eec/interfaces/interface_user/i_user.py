from abc import ABC


class IUser(ABC):
    """Interface for user class"""

    def __init__(
            self, user_id: str, user_name: str, role: str = '', salt: str = '',
            hashed_password: str = ''):
        self.user_id = user_id
        self.user_name = user_name
        self.role = role
        self.salt = salt
        self.hashed_password = hashed_password

    def get_user_id(self):
        return self.user_id

    def get_user_name(self):
        return self.user_name

    def get_user_role(self):
        return self.role

    def get_user_salt(self):
        return self.salt

    def get_user_hashed_password(self):
        return self.hashed_password

    def to_dict(self, include_password: bool = False):
        """Returns a dictionary representation of the user object"""
        data = {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'role': self.role,
        }
        if include_password:
            data['salt'] = self.salt
            data['hashed_password'] = self.hashed_password

        return data

    @classmethod
    def from_dict(cls, data: dict):
        """Returns a user object from a dictionary"""
        return cls(
            data['user_id'], data['user_name'], data['role'], data['salt'],
            data['hashed_password'])
