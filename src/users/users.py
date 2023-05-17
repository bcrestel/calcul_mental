import logging
from pathlib import Path

from src.io.pickle_io import read_from_pickle, write_to_pickle
from src.utils.constants import file_path

logger = logging.getLogger(__name__)


# TODO: add passwords
class Users:
    def __init__(self, filename: Path = "users.pickle"):
        self.filename = Path(file_path, filename)
        if not self.filename.exists():
            logger.warning(
                f"Could not find file {self.filename} for users."
                + " Creating it with empty list"
            )
            self.users = []
        else:
            self.users = read_from_pickle(self.filename)

    def does_user_exist(self, user: str) -> bool:
        return user.lower() in self.users

    def add_user(self, user: str):
        if not self.does_user_exist(user):
            self.users.append(user.lower())
        write_to_pickle(self.users, self.filename)


if __name__ == "__main__":
    all_users = Users()
    print(f"all_users in {all_users.filename}: {all_users.users}")
