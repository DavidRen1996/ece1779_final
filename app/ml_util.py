import boto3
from db.constants import *
from db import crud
from app import util

client = boto3.client('rekognition')


def find_nearby_matching_photo(interest_photo_location, gender_and_interest, latitude, longitude, distance_km):
    nearby_users = []
    user_locations = crud.select_nearby_users(gender_and_interest, latitude, longitude, distance_km)

    num_matches = 0

    for location in user_locations:
        nearby_username = location[USERNAME]
        nearby_profile_photo = util.get_profile_photo(nearby_username)
        if nearby_username is None or nearby_profile_photo is None:
            print('invalid username or no profile photo location found ' + str(nearby_username) + ':' +
                  str(nearby_profile_photo))
            continue

        if face_compare(interest_photo_location, nearby_profile_photo):
            num_matches += 1
            nearby_users.append((nearby_username, nearby_profile_photo))

        if num_matches == NUM_SUGGESTIONS:
            break

    return nearby_users


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
        SimilarityThreshold=70
    )

    if response['FaceMatches']:
        return True
    else:
        return False
