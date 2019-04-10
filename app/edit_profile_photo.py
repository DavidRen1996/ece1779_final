from flask import render_template, session, request, redirect, url_for
from app import webapp
from app.homeui import create_filename
from db.crud import *
from db.photo_info import PhotoInfo


@webapp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    return render_template('edit_profile.html')


# todo consolidate all s3 calls
s3 = boto3.client('s3')


# todo is this used?
@webapp.route('/edit_photo', methods=['GET', 'POST'])
def edit_photo():
    username = session['current_username']
    pword = session['current_password']

    new_profile_photo = request.files['new_profile']
    full_filename = create_filename(new_profile_photo)
    print(full_filename)
    # todo fix this, select profile image based on profile
    response_profile = select_all_photo_info_for_user(username, PHOTO_TYPE_PROFILE)
    profile_location = response_profile[0]
    profile_info = PhotoInfo(username, full_filename, PHOTO_TYPE_PROFILE, None, None)

    response = update_photo_info(profile_info)

    # todo don't forget to update the profile photo information
    response = overwrite_profile_photo(profile_location['photo_location'], profile_info)
    s3.upload_fileobj(new_profile_photo, 'dongxuren1779a2', full_filename)

    return redirect(url_for('load_homepage'))