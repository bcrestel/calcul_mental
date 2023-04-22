import sys
import logging

from src.users import Users
from src.constants import map_sym_text_op
from src.summary_file import SummaryFile

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Check for existing user and if not create new profile
    all_users = Users()
    logger.debug(f"all_users={all_users.users}")
    user_name = input("Quel est ton prénom? ")
    logger.debug(f"user_name={user_name}")
    if not all_users.does_user_exist(user_name):
        print(f"On dirait que c'est la première fois que tu te connectes, {user_name}.")
        create_profile = input("Veux-tu que je te créé un profil? [O/N] ")
        if create_profile == "O":
            print("C'est bon, je te créé un profil")
            all_users.add_user(user_name)
        else:
            print("Bye!")
            sys.exit()

    # Operations
    operation_sym = input("Quelle opération veux-tu travailler aujourd'hui? [*,+,-,/] ")
    if operation_sym not in map_sym_text_op.keys():
        print("Je ne comprends pas cette opération. Bye!")
        sys.exit()
    operation_type = map_sym_text_op[operation_sym]
    print(f"C'est bien compris. On va travailler l'opération: {operation_type.name}")
    logger.debug(f"Operation type: {operation_type}")

    # Obtain summary file
    summaryfile = SummaryFile(user_name=user_name, operation_type=operation_type)


