import logging
from pathlib import Path

from src.constants import file_path
from src.io.pickle_io import read_from_pickle, write_to_pickle

logger = logging.getLogger(__name__)

class Users:
    def __init__(self, filename: Path = "users.pickle"):
        self.filename = Path(file_path, filename)
        if not self.filename.exists():
            logger.warning(f"Could not find file {self.filename} for users." + \
                           " Creating it with empty list")
            self.users = []
        else:
            self.users = read_from_pickle(self.filename)

    def does_user_exist(self, user: str) -> bool:
        return user.lower() in self.users

    def add_user(self, user: str):
        if not self.does_user_exist(user):
            self.users.append(user.lower())
        write_to_pickle(self.users, self.filename)

