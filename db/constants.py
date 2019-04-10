S3_BUCKET_NAME = 'dongxuren1779a2'

PUBLIC_USER_INFO = 'public_user_info'
PRIVATE_USER_INFO = 'private_user_info'
PHOTO_INFO = 'photo_info'
USER_LOCATION = 'user_location'

USERNAME = 'username'
EMAIL = 'email'
NAME = 'name'
ENCRYPTED_PASSWORD = 'encrypted_password'
PHOTO_LOCATION = 'photo_location'
TYPE = 'type'
RELATED_PHOTOS_MAP = 'related_photos'
GENDER_AND_INTEREST = 'gender_and_interest'
BIRTHDAY = 'birthday'
REGION = 'region'
DESCRIPTION = 'description'
INTERESTED_PHOTOS_LIST = 'interested_photos_list'
PENDING_REQUESTS_MAP = 'pending_requests_map'
RECEIVED_INQUIRES = 'received_inquiries_map'
PHOTO_TYPE = 'photo_type'
PHOTO_ID_LOCATION='photo_id_location'
LATITUDE = 'latitude'
LONGITUDE = 'longitude'


PHOTO_TYPE_PROFILE = 1
PHOTO_TYPE_INTERESTED = 2

GENDER_AND_INTEREST_MF = 1
GENDER_AND_INTEREST_MM = 2
GENDER_AND_INTEREST_MB = 3
GENDER_AND_INTEREST_FF = 4
GENDER_AND_INTEREST_FM = 5
GENDER_AND_INTEREST_FB = 6

GENDER_INTEREST_MAP = {
    1: (5, 6),
    2: (2, 3),
    3: (2, 3, 5, 6),
    4: (4, 5),
    5: (1, 3),
    6: (1, 3, 4, 6)
}

DEGREE_OF_LATITUDE_IN_KM = 111
DEGREE_OF_LONGITUDE_IN_KM_AT_EQUATOR = 111.321
