class User:
    username = ""
    email = ""
    phone = ""
    is_logged_in = False

    def login(user_data: dict) -> None:
        User.is_logged_in = True
        User.username = user_data["username"]
        User.email = user_data["email"]
        User.phone = user_data["phone"]

    def logout() -> None:
        User.is_logged_in = False
        User.username = ""
        User.email = ""
        User.phone = ""
        
