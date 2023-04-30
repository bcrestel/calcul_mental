from src.users.users import Users

def create_new_user():
    user_name = input("Quel est le nom du nouvel utilisateur? ")
    YN = input(f"Je vais crééer une nouvelle entrée pour {user_name}, c'est bien ça? [Y/N] ")
    if YN == "Y":
        all_users = Users()
        all_users.add_user(user=user_name)
        print("C'est fait. Au revoir!")

if __name__ == "__main__":
    create_new_user()