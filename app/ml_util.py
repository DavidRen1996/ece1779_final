import boto3

client = boto3.client('rekognition')

S3_BUCKET_NAME = 'fill bucket name'


# returns a list of pairs of username and photo locations
def find_matching_photo(photo_location, list_of_username_and_photos_to_compare):
    matching_photo_location_and_username_pairs = []
    for pair in list_of_username_and_photos_to_compare:
        location = pair[1]

        if face_compare(photo_location, location):
            matching_photo_location_and_username_pairs.append(pair)
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
        SimilarityThreshold=30
    )

    if response['FaceMatches']:
        return True
    else:
        return False
