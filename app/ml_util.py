import boto3
from app.constants import *

client = boto3.client('rekognition')


# returns a list of photos locations and username pairs
def find_matching_photo(photo_location, list_of_photos_to_compare):
    matching_photo_location_and_username_pairs = []
    for location in list_of_photos_to_compare:
        print(photo_location,location[0])
        response = face_compare(photo_location, location[0])
        if response is not None:
            #print(response)
            face=response['FaceMatches']
            if face[0]['Similarity']>=70:
                #matching_photo_location_and_username_pairs.append(response)
                matching_photo_location_and_username_pairs.append(location)
    return matching_photo_location_and_username_pairs


def face_compare(photo_location, photo__to_compare_location):
    response = client.compare_faces(
        SourceImage={
            #'Bytes': b'bytes',
            'S3Object': {
                'Bucket': 'dongxuren1779a2',
                'Name': photo_location,
            }
        },
        TargetImage={
            #'Bytes': b'bytes',,.abens[
            'S3Object': {
                'Bucket': 'dongxuren1779a2',
                'Name': photo__to_compare_location,
            }
        },
        SimilarityThreshold=0.7
    )
    # todo parse the repsonse before returning
    return response
#print(face_compare('ben2019-04-04-05-11-22default.jpgjpg','david2019-04-04-03-43-07coke.jpgjpg'))
#res=face_compare('ben2019-04-04-05-11-22default.jpgjpg','dave2019-04-04-05-06-51default.jpgjpg')
#print(type(res['FaceMatches']))
#res=face_compare('ben2019-04-04-05-11-22default.jpgjpg','david2019-04-04-03-43-07coke.jpgjpg')
#k=res['FaceMatches']
#print(k[0]['Similarity'])
