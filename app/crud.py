import boto3
import json
from app.photo_info import PhotoInfo
from app.public_user_info import PublicUserInfo
from app.private_user_info import PrivateUserInfo

from boto3.dynamodb.conditions import Key,Attr

from app.constants import *

client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')


def get_public_user_info(username):
    return dynamodb.get_item(TableName=PUBLIC_USER_INFO, Key={'username': {'S': username}})


def update_public_user_info(public_user_info):
    table = dynamodb.Table(PUBLIC_USER_INFO)
    response = table.put_item(
        Item={
            USERNAME: public_user_info.username,
            EMAIL: public_user_info.email,
            NAME: public_user_info.name,
            BIRTHDAY: public_user_info.birthday,
            GENDER_AND_INTEREST: public_user_info.gender_and_interest,
            REGION: public_user_info.region,
            DESCRIPTION: public_user_info.description
        })
    return response


def update_private_user_info(private_user_info):
    table = dynamodb.Table(PRIVATE_USER_INFO)
    response = table.put_item(
        Item={
            USERNAME: private_user_info.username,
            ENCRYPTED_PASSWORD: private_user_info.encrypted_password,
            INTERESTED_PHOTOS_MAP: private_user_info.interested_photos_map,
            PENDING_REQUESTS_MAP: private_user_info.pending_requests_map,
            RELATED_PHOTOS_MAP: private_user_info.received_inquiries_map
        })
    return response
def overwrite_profile_photo(previous_name,photo_info):
    table = dynamodb.Table(PHOTO_INFO)
    response=table.update_item(
        Key={
            USERNAME: photo_info.username,
            PHOTO_LOCATION: previous_name
        },
        UpdateExpression='set PHOTO_TYPE=:r',
        ExpressionAttributeValues={
            ':r':PHOTO_TYPE_SELF
        },
        ReturnValues="UPDATED_NEW"

    )

def update_photo_info(photo_info):
    table = dynamodb.Table(PHOTO_INFO)
    response = table.put_item(
        Item={
            USERNAME: photo_info.username,
            PHOTO_LOCATION: photo_info.photo_location,
            PHOTO_TYPE: photo_info.photo_type,
            GENDER_AND_INTEREST: photo_info.gender_and_interest,
            RELATED_PHOTOS_MAP: photo_info.related_photos
        })
    return response


def select_public_user_info(username):
    table = dynamodb.Table(PUBLIC_USER_INFO)
    response = table.get_item(
        Key={
            USERNAME: username
        }
    )
    return response['Item']


def select_private_user_info(username):
    table = dynamodb.Table(PRIVATE_USER_INFO)
    response = table.get_item(
        Key={
            USERNAME: username
            #ENCRYPTED_PASSWORD:password
        }
    )
    print(response)
    if 'Item' not in response:
        return None
    else:
        return response['Item']
    #need modification here



def select_photo_info(username, photo_location):
    table = dynamodb.Table(PHOTO_INFO)
    response = table.get_item(
        Key={
            USERNAME: username,
            PHOTO_LOCATION: photo_location
        }
    )
    return response['Item']


# this returns a list of maps where each map is an photo_info object
def select_all_photo_info_for_user(username):
    table = dynamodb.Table(PHOTO_INFO)
    response = table.query(
        KeyConditionExpression=Key(USERNAME).eq(username)
    )
    return response['Items']

def select_profile_photo_info_for_user(username):
    table = dynamodb.Table(PHOTO_INFO)
    response = table.query(
        KeyConditionExpression=Key(USERNAME).eq(username),

        FilterExpression=Attr(PHOTO_TYPE).eq(PHOTO_TYPE_PROFILE)
    )
    return response['Items']

def select_all_profile_photo_info():
    table = dynamodb.Table(PHOTO_INFO)
    response = table.scan()

    return response['Items']

# todo add function to select all photos with the correct type for the user


def demo_update_public_user_info():
    public_user_info = PublicUserInfo('username1', 'email1', 'name1', '2000-01-01', GENDER_AND_INTEREST_MF, 'region1',
                                      'description1')
    response = update_public_user_info(public_user_info)
    print("demo_update_public_user_info succeeded:")
    print(json.dumps(response, indent=4))


def demo_update_private_user_info():
    private_user_info = PrivateUserInfo('username1', 'encrypted_password1',
                                        {'photo_location_of_username2': 'username2',
                                         'photo_location_of_username3': 'username3'},
                                        {}, {})
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
    response = select_private_user_info('username1')
    print("select_private_user_info succeeded:")
    print(response)
    print(response[USERNAME])


def demo_select_photo_info():
    response = select_photo_info('username1', 'no_photo_location')
    print("select_photo_info succeeded:")
    print(response)
    print(response[USERNAME]) 


def demo_select_all_photo_info_for_user():
    response = select_all_photo_info_for_user('username1')
    print("select_all_photo_info_for_user succeeded:")
    print(response)


#demo_update_photo_info()

#demo_select_photo_info()
