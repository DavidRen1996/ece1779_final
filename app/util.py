from db import crud
from db import constants


def get_profile_photo(username):
    photo_info = crud.select_all_photo_info_for_user(username, constants.PHOTO_TYPE_PROFILE)

    if photo_info is None:
        return None

    return photo_info[0][constants.PHOTO_LOCATION]
