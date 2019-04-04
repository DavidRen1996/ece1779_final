import boto3

from werkzeug.security import generate_password_hash, check_password_hash
from boto3.dynamodb.conditions import Key, Attr

from db.constants import *

client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')


def update_public_user_info(public_user_info):
    table = dynamodb.Table(PUBLIC_USER_INFO)
    response = table.put_item(
        Item={
            USERNAME: public_user_info.username,
            EMAIL: public_user_info.email,
            NAME: public_user_info.name,
            BIRTHDAY: public_user_info.birthday,
            PHOTO_ID_LOCATION: public_user_info.photo_id_location,
            GENDER_AND_INTEREST: public_user_info.gender_and_interest,
            REGION: public_user_info.region,
            DESCRIPTION: public_user_info.description
        })
    return response


def update_private_user_info(private_user_info):
    encrypted_password = generate_password_hash(private_user_info.password)

    table = dynamodb.Table(PRIVATE_USER_INFO)
    response = table.put_item(
        Item={
            USERNAME: private_user_info.username,
            ENCRYPTED_PASSWORD: encrypted_password,
            INTERESTED_PHOTOS_LIST: private_user_info.interested_photos_map,
            PENDING_REQUESTS_MAP: private_user_info.pending_requests_map,
            RELATED_PHOTOS_MAP: private_user_info.received_inquiries_map
        })
    return response


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
    return resolve_response(response)


def select_all_public_user_info(gender_and_interest):
    table = dynamodb.Table(PUBLIC_USER_INFO)
    interest_list = GENDER_INTEREST_MAP[gender_and_interest]
    response = table.scan(
        FilterExpression=Attr(GENDER_AND_INTEREST).eq(interest_list[0]) | Attr(GENDER_AND_INTEREST).eq(
            interest_list[1])
    )
    return resolve_response(response)


def select_private_user_info(username, password):
    table = dynamodb.Table(PRIVATE_USER_INFO)
    response = table.get_item(
        Key={
            USERNAME: username
        }
    )

    if 'Item' not in response:
        print('username ' + username + ' not found')
        return None

    private_info = response['Item']

    if not check_password_hash(private_info[ENCRYPTED_PASSWORD], password):
        print('password for ' + username + 'was incorrect')
        return None

    return private_info


def select_photo_info(username, photo_location):
    table = dynamodb.Table(PHOTO_INFO)
    response = table.get_item(
        Key={
            USERNAME: username,
            PHOTO_LOCATION: photo_location
        }
    )
    return resolve_response(response)


# this returns a list of maps where each map is an photo_info object
def select_all_photo_info_for_user(username, photo_type):
    table = dynamodb.Table(PHOTO_INFO)
    response = table.query(
        KeyConditionExpression=Key(USERNAME).eq(username),
        FilterExpression=Attr(PHOTO_TYPE).eq(photo_type),
    )
    return resolve_response(response)


def resolve_response(response):
    if 'Item' in response:
        return response['Item']

    if 'Items' in response:
        return response['Items']

    return None
