from abc import ABC

class UserDbBase(ABC):
    def __init__(self, id, username, email, hashed_password, type, create_date) -> None:
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.type = type
        self.create_date = create_date
    

