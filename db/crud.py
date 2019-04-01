import boto3
import json
from db.photo_info import PhotoInfo

from db.constants import *

client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')


def get_public_user_info(username):
    return dynamodb.get_item(TableName=PUBLIC_USER_INFO, Key={'username': {'S': username}})


def update_photo_info(photo_info):
    table = dynamodb.Table(PHOTO_INFO)
    response = table.put_item(
        Item={
            USERNAME: photo_info.username,
            PHOTO_LOCATION: photo_info.photo_location,
            TYPE: photo_info.type,
            RELATED_PHOTOS: photo_info.related_photos
        })
    return response


def demo_update_photo_info():
    photo_info = PhotoInfo("username1", "no_photo_location", 1,
                           {"photo_of_username2": "username2", "photo_of_username3": "username3"})
    response = update_photo_info(photo_info)
    print("PutItem succeeded:")
    print(json.dumps(response, indent=4))


demo_update_photo_info()
