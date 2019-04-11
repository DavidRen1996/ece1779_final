class PublicUserInfo:
    def __init__(self, username, email, name, photo_id_location, birthday, gender_and_interest, region, description):
        self.username = username
        self.email = email
        self.name = name
        self.photo_id_location = photo_id_location
        self.birthday = birthday  # YYYY-MM_DD format enforced
        self.gender_and_interest = gender_and_interest  # MF MM MB FF FM FB - B is Both
        self.region = region
        self.description = description
