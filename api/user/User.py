from dataclasses import dataclass
import json, pathlib

USERS_DB = pathlib.Path(__file__).resolve().parent / "Users.json"

@dataclass
class UserDB:
    id: int
    apkey: str
    password: str
    role: str

class UserRepo:
    def __init__(self, users: list[UserDB]):
        self.users = users

    @staticmethod
    def load_users() -> "UserRepo":
        data = json.loads(USERS_DB.read_bytes().decode("utf-8"))
        users = [UserDB(**u) for u in data["users"]]
        return UserRepo(users)

    def get_by_apkey(self, key: str) -> UserDB | None:
        # we can load users into a dict when the UserRepo is initalized
        # accessing dictionary is faster than looping each time a new user logs in
        for user in self.users:
            if user.apkey == key:
                return user

        return None


