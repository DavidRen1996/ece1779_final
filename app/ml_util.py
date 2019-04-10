import boto3
from db.constants import *

client = boto3.client('rekognition')


# todo explain how this works
# returns a list of photos locations and username pairs
def find_matching_photo(photo_location, list_of_photos_to_compare):
    matching_photo_location_and_username_pairs = []
    for locationAndName in list_of_photos_to_compare:
        print(photo_location, locationAndName[0])
        response = face_compare(photo_location, locationAndName[0])
        if response is not None:
            matching_photo_location_and_username_pairs.append(locationAndName)
    return matching_photo_location_and_username_pairs


def face_compare(photo_location, photo__to_compare_location):
    response = client.compare_faces(
        SourceImage={
            'S3Object': {
                'Bucket': S3_BUCKET_NAME,
                'Name': photo_location,
            }
        },
        TargetImage={
            'S3Object': {
                'Bucket': S3_BUCKET_NAME,
                'Name': photo__to_compare_location,
            }
        },
        SimilarityThreshold=70
    )
    return response

# print(face_compare('ben2019-04-04-05-11-22default.jpgjpg','david2019-04-04-03-43-07coke.jpgjpg'))
# res=face_compare('ben2019-04-04-05-11-22default.jpgjpg','dave2019-04-04-05-06-51default.jpgjpg')
# print(type(res['FaceMatches']))
# res=face_compare('ben2019-04-04-05-11-22default.jpgjpg','david2019-04-04-03-43-07coke.jpgjpg')
# k=res['FaceMatches']
# print(k[0]['Similarity'])
