from db.constants import *


class PhotoInfo:
    def __init__(self, username, photo_location, type, related_photos):
        self.username = username
        self.photo_location = photo_location
        self.type = type
        self.related_photos = related_photos


def create_photo_info(username, photo_location, type, related_photos):
    item = {}
    item[USERNAME] = username
    item[PHOTO_LOCATION] = photo_location
    item[TYPE] = type
    item[RELATED_PHOTOS] = related_photos
    return item
