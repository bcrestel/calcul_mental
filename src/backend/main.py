import sys
import logging

from src.users.users import Users
from src.utils.constants import map_sym_text_op
from src.backend.result_file import ResultFile
from src.backend.quiz_runner import quiz_runner
from src.backend.get_summary_files import get_summary_files

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(filename)s--l.%(lineno)d: %(message)s')
logger = logging.getLogger(__name__)


def main():
    # Get input parameters

    # TODO: integrate within Users
    # Check for existing user and if not create new profile
    all_users = Users()
    logger.debug(f"all_users={all_users.users}")
    user_name = input("Quel est ton prénom? ").lower()
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
    operation_sym = input("\nQuelle opération veux-tu travailler aujourd'hui? [*,+,-,/] ")
    if operation_sym not in map_sym_text_op.keys():
        print("Je ne comprends pas cette opération. Bye!")
        sys.exit()
    operation_type = map_sym_text_op[operation_sym]
    print(f"C'est bien compris. On va travailler l'opération: {operation_type.name}")
    logger.debug(f"Operation type: {operation_type}")
    # Masking
    min_b = int(input("\nQuelle est la plus PETITE table que tu veux travailler? "))
    max_b = int(input("Quelle est la plus GRANDE table que tu veux travailler? "))
    if min_b > max_b:
        raise ValueError(f"La plus petite table est plus grande que la plus grande ")
    # Sample questions
    nb_questions = int(input("Combien de questions veux-tu faire aujourd'hui? "))

    summaryfile, summaryfile_session = get_summary_files(
        user_name=user_name,
        operation_type=operation_type,
        min_b=min_b,
        max_b=max_b,
        nb_questions=nb_questions,
    )

    # Run the quiz
    _ = input("Es-tu prêt(e)? Appuie sur 'RETURN' quand tu veux démarrer.\n")
    answers, time_spent = quiz_runner(
        first_numbers=summaryfile_session["a"].tolist(),
        second_numbers=summaryfile_session["b"].tolist(),
        operation=summaryfile_session["op"].unique().item()
    )

    # Process results
    summaryfile_session["answers"] = answers
    logger.debug(summaryfile_session)
    result_file = ResultFile(
        user_name=user_name,
        result_table=summaryfile_session,
        total_time_spent=time_spent,
    )
    print(result_file.analyze_results())

    # Log all files and results
    summaryfile.update_from_answers(result_table=result_file.result_table)
    result_file.update_logfile()


if __name__ == "__main__":
    main()
