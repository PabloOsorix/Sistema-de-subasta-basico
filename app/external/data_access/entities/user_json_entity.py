from app.external.data_access.interfaces.user import UserDbBase



class UserJsonEntity(UserDbBase):
    def __init__(self, id, username, email, hashed_password, type, create_date) -> None:
        self.id = id
        self.username =username
        self.email = email
        self.hashed_password = hashed_password
        self.type = type
        self.create_date = create_date
        
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.hashed_password,
            "type": self.type,
            "create_date": self.create_date
        }
    
    
