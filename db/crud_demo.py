import json

from db.photo_info import PhotoInfo
from db.public_user_info import PublicUserInfo
from db.private_user_info import PrivateUserInfo

from db.constants import *
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
    photo_info = PhotoInfo('username1', 'no_photo_location', PHOTO_TYPE_SELF, GENDER_AND_INTEREST_MF,
                           {'photo_location_of_username2': 'username2', 'photo_location_of_username3': 'username3'})
    response = update_photo_info(photo_info)
    print("update_photo_info succeeded:")
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
    response = select_all_photo_info_for_user('username1', PHOTO_TYPE_SELF)
    print("select_all_photo_info_for_user succeeded:")
    print(response)


select_all_public_user_info(GENDER_AND_INTEREST_MF)
