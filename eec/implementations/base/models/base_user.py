from eec.interfaces.interface_user.i_user import IUser


class BaseUser(IUser):

    def __init__(
            self, user_id: str, user_name: str, role: str = '',
            hashed_password: str = ''):
        super().__init__(user_id, user_name, role, hashed_password)
