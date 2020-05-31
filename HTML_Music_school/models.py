class Course:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Users:
    def __init__(self, id, name, password, course, access_level):
        self.id = id
        self.name = name
        self.password = password
        self.course = course
        self.access_level = access_level


class Edit_Users_Access_Level:
    def __init__(self, id, name, access_level):
        self.id = id
        self.name = name
        self.access_level = access_level


ACCESS_LEVEL = ['Master', 'Instructor', 'Student']