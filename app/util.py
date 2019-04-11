from db import crud
from db import constants
import boto3

s3 = boto3.client('s3')


def get_profile_photo(username):
    photo_info = crud.select_all_photo_info_for_user(username, constants.PHOTO_TYPE_PROFILE)

    if not photo_info:
        return None

    return photo_info[0][constants.PHOTO_LOCATION]


def get_photo_url(photo_name):
    return s3.generate_presigned_url('get_object',
                                     Params={
                                         'Bucket': constants.S3_BUCKET_NAME,
                                         'Key': photo_name,
                                     },
                                     ExpiresIn=3600)
