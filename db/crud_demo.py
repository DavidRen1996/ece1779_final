import json

from db.photo_info import PhotoInfo
from db.public_user_info import PublicUserInfo
from db.private_user_info import PrivateUserInfo
from db.user_location import UserLocation

from db.crud import *


def demo_update_public_user_info():
    public_user_info = PublicUserInfo('username1', 'email1', 'name1', '2000-01-01', GENDER_AND_INTEREST_MF, 'region1',
                                      'description1')
    response = update_public_user_info(public_user_info)
    print("demo_update_public_user_info succeeded:")
    print(json.dumps(response, indent=4))


def demo_update_private_user_info():
    private_user_info = PrivateUserInfo('username4', 'password4',
                                        {'location_of_interested_photo1', 'location_of_interested_photo2'}, {}, {})
    response = update_private_user_info(private_user_info)
    print('update_private_user_info succeeded:')
    print(json.dumps(response, indent=4))


def demo_update_photo_info():
    photo_info = PhotoInfo('username1', 'no_photo_location', PHOTO_TYPE_PROFILE, GENDER_AND_INTEREST_MF,
                           {'photo_location_of_username2': 'username2', 'photo_location_of_username3': 'username3'})
    response = update_photo_info(photo_info)
    print("update_photo_info succeeded:")
    print(json.dumps(response, indent=4))


def demo_update_user_location():
    user_location = UserLocation(1, 'username1', 10.01, 12.01)
    response = update_user_location(user_location)
    print("update_user_location succeeded:")
    print(json.dumps(response, indent=4))


def demo_select_public_user_info():
    response = select_public_user_info('username1')
    print("select_public_user_info succeeded:")
    print(response)
    print(response[USERNAME])


def demo_select_private_user_info():
    response = select_private_user_info('username4', 'password4')
    print("select_private_user_info succeeded:")
    print(response)
    print(response[USERNAME])


def demo_select_photo_info():
    response = select_photo_info('username1', 'no_photo_location')
    print("select_photo_info succeeded:")
    print(response)
    print(response[USERNAME])


def demo_select_all_photo_info_for_user():
    response = select_all_photo_info_for_user('username1', PHOTO_TYPE_PROFILE)
    print("select_all_photo_info_for_user succeeded:")
    print(response)


def demo_select_nearby_users():
    response = select_nearby_users(1, 10.05, 12.05, 300)
    print("demo_select_nearby_users succeeded:")
    print(response)


demo_select_nearby_users()
