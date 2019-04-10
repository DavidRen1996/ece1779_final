from flask import Flask,render_template,session,request, redirect, url_for, g
from app import webapp
import boto3
import datetime
from app.homeui import create_filename
from app.constants import *
from app.photo_info import PhotoInfo
from app.crud import *
@webapp.route('/post_photo', methods=['GET', 'POST'])
def post_photo():
    s3=boto3.client('s3')
    new_file=request.files['postimage']
    new_file.seek(0)
    username=session['current_username']
    full_filename=create_filename(new_file)
    s3.upload_fileobj(new_file,'dongxuren1779a2',full_filename)
    photo_infos = PhotoInfo(username, full_filename, PHOTO_TYPE_SELF,None,None)
    response = update_photo_info(photo_infos)

    response_public=select_public_user_info(username)
    response_photo=select_all_photo_info_for_user(username)
    #need modification here
    post_username=response_public[USERNAME]
    post_region=response_public[REGION]
    post_email=response_public[EMAIL]
    post_bio=response_public[DESCRIPTION]
    response_profile=select_profile_photo_info_for_user(username)

    profile_location=response_profile[0]
    photo_location=profile_location[PHOTO_LOCATION]
    url_profile=s3.generate_presigned_url('get_object',
                                      Params={
                                          'Bucket':'dongxuren1779a2',
                                          'Key':photo_location,

                                      },
                                      ExpiresIn=3600)
    url_post_list=[]
    for index in response_photo:
        location=index[PHOTO_LOCATION]
        url=s3.generate_presigned_url('get_object',
                                      Params={
                                          'Bucket':'dongxuren1779a2',
                                          'Key':location,

                                      },
                                      ExpiresIn=3600)
        url_post_list.append(url)


    return render_template('home.html',username=post_username,bio=post_bio,email=post_email,region=post_region,url_list=url_post_list,url_profile=url_profile)
