class PublicUserInfo:
    def __init__(self, username, email, name, birthday, gender_and_interest, description):
        self.username = username
        self.email = email
        self.name = name
        self.birthday = birthday  # YYYY-MM_DD format enforced
        self.gender_and_interest = gender_and_interest # MF MM MB FF FM FB - B is Both
        self.description = description
