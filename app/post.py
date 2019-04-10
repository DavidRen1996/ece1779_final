from flask import Flask, render_template, session, request, redirect, url_for, g
from app import webapp
from app.homeui import create_filename
from db.crud import *
from db.photo_info import PhotoInfo

s3 = boto3.client('s3')


@webapp.route('/post_photo', methods=['GET', 'POST'])
def post_photo():
    new_file = request.files['postimage']
    new_file.seek(0)
    username = session['current_username']
    full_filename = create_filename(new_file)
    s3.upload_fileobj(new_file, 'dongxuren1779a2', full_filename)
    photo_infos = PhotoInfo(username, full_filename, PHOTO_TYPE_PROFILE, None, None)
    response = update_photo_info(photo_infos)

    response_public = select_public_user_info(username)
    response_photo = select_all_photo_info_for_user(username)

    # todo need modification here
    post_username = response_public[USERNAME]
    post_region = response_public[REGION]
    post_email = response_public[EMAIL]
    post_bio = response_public[DESCRIPTION]
    response_profile = select_all_photo_info_for_user(username, PHOTO_TYPE_PROFILE)

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

    return render_template('home.html', username=post_username, bio=post_bio, email=post_email, region=post_region,
                           url_list=url_post_list, url_profile=url_profile)


# this is used to search nearby and find the people you might be interested in
@webapp.route('/post_photo_with_location', methods=['POST'])
def post_photo_with_location():
    latitude = request.files['latitude']
    longitude = request.files['longitude']
    distance_km = request.files['distance_km']
    username = session['current_username']
    new_file = request.files['postimage']
    new_file.seek(0)
    full_filename = create_filename(new_file)

    s3.upload_fileobj(new_file, 'dongxuren1779a2', full_filename)
    photo_infos = PhotoInfo(username, full_filename, PHOTO_TYPE_PROFILE, None, None)
    update_photo_info(photo_infos)

    response_public = select_public_user_info(username)

    response_suggested_users = select_nearby_users()

    # todo need modification here
    post_username = response_public[USERNAME]
    post_region = response_public[REGION]
    post_email = response_public[EMAIL]
    post_bio = response_public[DESCRIPTION]
    response_profile = select_profile_photo_info_for_user(username)

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

    return render_template('home.html', username=post_username, bio=post_bio, email=post_email, region=post_region,
                           url_list=url_post_list, url_profile=url_profile)
