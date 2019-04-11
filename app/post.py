from flask import Flask, render_template, session, request, redirect, url_for, g
from app import webapp
from app.util import get_photo_url
from app.homeui import create_filename
from db.crud import *
from db.photo_info import PhotoInfo



@webapp.route('/post_photo', methods=['GET', 'POST'])
def post_photo():
    new_file = request.files['postimage']
    new_file.seek(0)
    username = session['current_username']
    photo_name = create_filename(new_file)
    s3.upload_fileobj(new_file, S3_BUCKET_NAME, photo_name)

    response_public = select_public_user_info(username)

    photo_info = PhotoInfo(username, photo_name, PHOTO_TYPE_POST, response_public[GENDER_AND_INTEREST], None)
    update_photo_info(photo_info)

    response_photo = select_all_photo_info_for_user(username, PHOTO_TYPE_POST)

    # todo need modification here
    post_username = response_public[USERNAME]
    post_region = response_public[REGION]
    post_email = response_public[EMAIL]
    post_bio = response_public[DESCRIPTION]
    response_profile = select_all_photo_info_for_user(username, PHOTO_TYPE_PROFILE)

    profile_location = response_profile[0]
    photo_location = profile_location[PHOTO_LOCATION]
    url_profile = get_photo_url(photo_location)
    url_post_list = []
    for photo_info in response_photo:
        location = photo_info[PHOTO_LOCATION]
        url = get_photo_url(location)
        url_post_list.append(url)

    return render_template('home.html', username=post_username, bio=post_bio, email=post_email, region=post_region,
                           url_list=url_post_list, url_profile=url_profile)
