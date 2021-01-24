from typing import Optional


FIRST_NAME = 0
LAST_NAME = 1
EMAIL = 2
USERNAME = 3
WEBSITE = 4
ROLE = 5
NICKNAME = 6
BIO = 7
PASSWORD = 8


class Employee:
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    username: Optional[str]
    website: Optional[str]
    role: Optional[str]
    nickname: Optional[str]
    bio: Optional[str]
    password: Optional[str]

    def __init__(self, employee_data):
        # TODO safe getting
        self.first_name = employee_data[FIRST_NAME]
        self.last_name = employee_data[LAST_NAME]
        self.email = employee_data[EMAIL]
        self.username = employee_data[USERNAME]
        self.website = employee_data[WEBSITE]
        self.role = employee_data[ROLE]
        self.nickname = employee_data[NICKNAME]
        self.bio = employee_data[BIO]
        self.password = employee_data[PASSWORD]

    def __str__(self):
        return self.data

    def __repr__(self):
        return str(self.data)
