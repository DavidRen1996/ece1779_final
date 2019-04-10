from flask import Flask,render_template,session,request, redirect, url_for, g
from app import webapp
import boto3
import datetime
from app.homeui import create_filename
from app.constants import *
from app.photo_info import PhotoInfo
from app.crud import *
@webapp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    return render_template('edit_profile.html')
@webapp.route('/edit_photo', methods=['GET', 'POST'])
def edit_photo():
    s3=boto3.client('s3')
    username=session['current_username']
    pword=session['current_password']
    new_profile_photo=request.files['new_profile']
    full_filename=create_filename(new_profile_photo)
    print(full_filename)
    response_profile=select_profile_photo_info_for_user(username)
    profile_location=response_profile[0]
    profile_info=PhotoInfo(username, full_filename, PHOTO_TYPE_PROFILE,None,None)

    response = update_photo_info(profile_info)

    response =overwrite_profile_photo(profile_location['photo_location'],profile_info)
    s3.upload_fileobj(new_profile_photo,'dongxuren1779a2',full_filename)

    return redirect(url_for('load_homepage'))
