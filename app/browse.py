from flask import Flask,render_template,session,request, redirect, url_for, g
from app import webapp
from app.crud import *
from app.constants import *
from app.public_user_info import PublicUserInfo
from app.private_user_info import PrivateUserInfo
from app.photo_info import PhotoInfo
from app import ml_util
import datetime
import boto3
import os
@webapp.route('/browse/<photo_username>', methods=['GET', 'POST'])
def browse(photo_username):
    s3=boto3.client('s3')
    print(photo_username)
    response_public=select_public_user_info(photo_username)
    response_photo=select_all_photo_info_for_user(photo_username)
    #need modification here
    post_username=response_public[USERNAME]
    post_region=response_public[REGION]
    post_email=response_public[EMAIL]
    post_bio=response_public[DESCRIPTION]
    post_birth=response_public[BIRTHDAY]
    post_interest=response_public[GENDER_AND_INTEREST]
    post_gender=[]
    post_interest=int(post_interest)
    if post_interest<=3:
        post_gender.append('male')
        if post_interest==3:
            post_gender.append('both')
        if post_interest==2:
            post_gender.append('male')
        if post_interest==1:
            post_gender.append('female')
    else:
        post_gender.append('female')
        if post_interest==6:
            post_gender.append('both')
        if post_interest==5:
            post_gender.append('male')
        if post_interest==4:
            post_gender.append('female')


    response_profile=select_profile_photo_info_for_user(photo_username)

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
    return  render_template('browse.html',username=post_username,bio=post_bio,email=post_email,region=post_region,url_list=url_post_list,url_profile=url_profile,birthday=post_birth,post_gender=post_gender)
