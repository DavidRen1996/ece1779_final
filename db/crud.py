import boto3

from werkzeug.security import generate_password_hash, check_password_hash
from boto3.dynamodb.conditions import Key, Attr
import math
from decimal import Decimal

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


def update_user_location(user_location):
    table = dynamodb.Table(USER_LOCATION)
    response = table.put_item(
        Item={
            GENDER_AND_INTEREST: user_location.gender_and_interest,
            USERNAME: user_location.username,
            LATITUDE: Decimal(str(user_location.latitude)),
            LONGITUDE: Decimal(str(user_location.longitude))
        })
    return response


def overwrite_profile_photo(previous_name, photo_info):
    table = dynamodb.Table(PHOTO_INFO)
    response = table.update_item(
        Key={
            USERNAME: photo_info.username,
            PHOTO_LOCATION: previous_name
        },
        UpdateExpression='set PHOTO_TYPE=:r',
        ExpressionAttributeValues={
            ':r': PHOTO_TYPE_PROFILE
        },
        ReturnValues="UPDATED_NEW"
    )
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


# only use this if the username is already in the session
def select_private_user_info(username):
    table = dynamodb.Table(PRIVATE_USER_INFO)
    response = table.get_item(
        Key={
            USERNAME: username
        }
    )

    if 'Item' not in response:
        print('username ' + username + ' not found')
        return None

    return response['Item']


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


# this functions needs the lati and long to be in decimal degrees
def select_nearby_users(gender_and_interest, latitude, longitude, distance_km):
    latitude_delta = distance_km / DEGREE_OF_LATITUDE_IN_KM
    longitude_delta = get_longitude_degree_from_distance(distance_km, latitude)
    interest_list = GENDER_INTEREST_MAP[gender_and_interest]

    table = dynamodb.Table(PHOTO_INFO)
    response = table.scan(
        FilterExpression=Key(GENDER_AND_INTEREST).eq(interest_list[0]) | Key(GENDER_AND_INTEREST).eq(
            interest_list[1]) & Attr(LATITUDE).between(Decimal(str(latitude - latitude_delta)),
                                                       Decimal(str(latitude + latitude_delta))) & Attr(
            LONGITUDE).between(Decimal(str(longitude - longitude_delta)), Decimal(str(longitude + longitude_delta)))
    )

    return resolve_response(response)


def resolve_response(response):
    if 'Item' in response:
        return response['Item']

    if 'Items' in response:
        return response['Items']

    return None


def get_longitude_degree_from_distance(distance_km, latitude):
    one_degree_longitude_km = math.fabs(math.cos(latitude)) * 111.321

    if one_degree_longitude_km == 0:
        return 0
    return distance_km / one_degree_longitude_km
