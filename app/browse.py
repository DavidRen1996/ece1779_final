from flask import render_template
from app import webapp
from db.crud import *
from db.constants import *
import boto3

s3 = boto3.client('s3')


@webapp.route('/browse/<photo_username>', methods=['GET', 'POST'])
def browse(photo_username):
    print(photo_username)
    response_public = select_public_user_info(photo_username)
    response_photo = select_all_photo_info_for_user(photo_username)
    # todo need modification here
    post_username = response_public[USERNAME]
    post_region = response_public[REGION]
    post_email = response_public[EMAIL]
    post_bio = response_public[DESCRIPTION]
    post_birth = response_public[BIRTHDAY]
    post_interest = response_public[GENDER_AND_INTEREST]
    post_gender = []
    post_interest = int(post_interest)
    if post_interest <= 3:
        post_gender.append('male')
        if post_interest == 3:
            post_gender.append('both')
        if post_interest == 2:
            post_gender.append('male')
        if post_interest == 1:
            post_gender.append('female')
    else:
        post_gender.append('female')
        if post_interest == 6:
            post_gender.append('both')
        if post_interest == 5:
            post_gender.append('male')
        if post_interest == 4:
            post_gender.append('female')

    response_profile = select_all_photo_info_for_user(photo_username, PHOTO_TYPE_POST)

    profile_location = response_profile[0]
    photo_location = profile_location[PHOTO_LOCATION]
    url_profile = s3.generate_presigned_url('get_object',
                                            Params={
                                                'Bucket': S3_BUCKET_NAME,
                                                'Key': photo_location,

                                            },
                                            ExpiresIn=3600)
    url_post_list = []
    for index in response_photo:
        location = index[PHOTO_LOCATION]
        url = s3.generate_presigned_url('get_object',
                                        Params={
                                            'Bucket': S3_BUCKET_NAME,
                                            'Key': location,

                                        },
                                        ExpiresIn=3600)
        url_post_list.append(url)
    return render_template('browse.html', username=post_username, bio=post_bio, email=post_email, region=post_region,
                           url_list=url_post_list, url_profile=url_profile, birthday=post_birth,
                           post_gender=post_gender)
