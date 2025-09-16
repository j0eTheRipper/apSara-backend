from dataclasses import dataclass
import json, pathlib

USERS_DB = pathlib.Path("Users.json")

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
        data = json.loads(USERS_DB.read_text(encoding="utf-8"))
        users = [UserDB(**u) for u in data]
        return UserRepo(users)

    def get_by_apkey(self, key: str) -> UserDB | None:
        for user in self.users:
            if user.apkey == key:
                return user

        return None


