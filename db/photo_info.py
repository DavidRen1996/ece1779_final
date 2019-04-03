class PhotoInfo:
    def __init__(self, username, photo_location, gender_and_interest, related_photos):
        self.username = username
        self.photo_location = photo_location
        self.gender_and_interest = gender_and_interest
        self.related_photos = related_photos

    def cast_map(self, **entries):
        self.__dict__.update(entries)
