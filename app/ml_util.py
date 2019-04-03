import boto3
from db.constants import *

client = boto3.client('rekognition')


# returns a list of photos locations and username pairs
def find_matching_photo(photo_location, list_of_photos_to_compare):
    matching_photo_location_and_username_pairs = []
    for location in list_of_photos_to_compare:
        response = face_compare(photo_location, location)
        if response is not None:
            matching_photo_location_and_username_pairs.append(response)
    return matching_photo_location_and_username_pairs


def face_compare(photo_location, photo__to_compare_location):
    response = client.compare_faces(
        SourceImage={
            'Bytes': b'bytes',
            'S3Object': {
                'Bucket': S3_BUCKET_NAME,
                'Name': photo_location,
            }
        },
        TargetImage={
            'Bytes': b'bytes',
            'S3Object': {
                'Bucket': S3_BUCKET_NAME,
                'Name': photo__to_compare_location,
            }
        },
        SimilarityThreshold=0.7
    )
    # todo parse the repsonse before returning
    return response
