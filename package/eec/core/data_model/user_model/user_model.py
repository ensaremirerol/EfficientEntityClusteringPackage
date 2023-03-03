class UserModel():
    """ User model class """

    def __init__(
            self, user_id: str, username: str, role: str = '',
            hashed_password: str = ''):
        self.user_id: str = user_id
        self.username: str = username
        self.role: str = role
        self.hashed_password: str = hashed_password

    def __str__(self):
        return f"UserModel({self.user_id}, {self.username})"

    def __repr__(self):
        return f"UserModel({self.user_id}, {self.username})"

    def __eq__(self, other):
        if not isinstance(other, UserModel):
            return False
        return self.user_id == other.user_id

    def to_dict(self, include_password: bool = False):
        """Returns a dictionary representation of the user object"""
        data = {
            'user_id': self.user_id,
            'username': self.username,
            'role': self.role,
        }
        if include_password:
            data['hashed_password'] = self.hashed_password

        return data

    @classmethod
    def from_dict(cls, data: dict):
        """Returns a user object from a dictionary"""
        return cls(
            user_id=data['user_id'], username=data['username'],
            role=data['role'], hashed_password=data['hashed_password'])
