from flask import render_template, session, request, redirect, url_for
from app import webapp
from db import crud
from db import constants
from db.public_user_info import PublicUserInfo
from db.private_user_info import PrivateUserInfo
from db.photo_info import PhotoInfo
from app import ml_util
import datetime
import boto3
import os
from googletrans import Translator

s3 = boto3.client('s3')


# logout
@webapp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('main'))


# take the uname and pword from login html, check if is already registered and update session
@webapp.route('/login_submit', methods=['POST'])
def login_submit():
    if 'login_username' in request.form and 'login_password' in request.form:
        # check if registered
        session['current_username'] = request.form['login_username']
        session['current_password'] = request.form['login_password']
        uname = request.form['login_username']
        pword = request.form['login_password']
        response = crud.select_private_user_info(uname)
        if response is None:
            print('current not registered')
            error = 'current not registered'
            return render_template('loginpage.html', error=error)
        else:
            extracted_password = response[constants.ENCRYPTED_PASSWORD]
            if extracted_password == pword:
                print('login success')
                return redirect(url_for('load_homepage'))
            else:
                print('password not match')
                error = 'password not match'
                return render_template('loginpage.html', error=error)


def filename_extension(filename):
    _, file_extension = os.path.splitext(filename)
    return file_extension[1:]


def create_filename(upload_file):
    username = session['current_username']
    filename = upload_file.filename
    store_ext = filename_extension(upload_file.filename)
    total_filename = username + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + filename
    return total_filename


@webapp.route('/new_submit', methods=['POST'])
def new_submit():
    session['current_username'] = request.form['signup_username']
    session['current_password'] = request.form['signup_password']
    name = request.form['signup_name']
    username = request.form['signup_username']
    password = request.form['signup_password']
    year = request.form['year']
    month = request.form['month']
    birthday = year + month
    print(birthday)
    sex = request.form['Sex']
    interest = request.form['interest']
    Sex = constants.GENDER_AND_INTEREST
    if sex == 'male' and interest == 'male':
        Sex = constants.GENDER_AND_INTEREST_MM
    if sex == 'male' and interest == 'female':
        Sex = constants.GENDER_AND_INTEREST_MF
    if sex == 'male' and interest == 'both':
        Sex = constants.GENDER_AND_INTEREST_MB
    if sex == 'female' and interest == 'male':
        Sex = constants.GENDER_AND_INTEREST_FM
    if sex == 'female' and interest == 'female':
        Sex = constants.GENDER_AND_INTEREST_FF
    if sex == 'female' and interest == 'both':
        Sex = constants.GENDER_AND_INTEREST_FB

    session['current_sex'] = request.form['Sex']
    Bio = request.form['Bio']
    email = request.form['email']
    region = request.form['region']
    profile_photo = request.files['Profile_Photo']
    full_filename = create_filename(profile_photo)
    s3.upload_fileobj(profile_photo, constants.S3_BUCKET_NAME, full_filename)
    public_info = PublicUserInfo(username, email, name, full_filename, birthday, Sex, region,
                                 Bio)
    response_public = crud.update_public_user_info(public_info)
    private_info = PrivateUserInfo(username, password, None, None, None)
    response_private = crud.update_private_user_info(private_info)
    photo_infos = PhotoInfo(username, full_filename, constants.PHOTO_TYPE_POST, Sex, None)
    response = crud.update_photo_info(photo_infos)

    return redirect(url_for('load_homepage'))


@webapp.route('/post', methods=['POST', 'GET'])
def post():
    return render_template('post.html')


@webapp.route('/load_homepage', methods=['POST', 'GET'])
def load_homepage():
    # use username to get posted image and user profile
    username = session['current_username']
    response_public = crud.select_public_user_info(username)
    response_photo = crud.select_all_photo_info_for_user(username, constants.PHOTO_TYPE_POST)
    # todo need modification here
    post_username = response_public[constants.USERNAME]
    post_region = response_public[constants.REGION]
    post_email = response_public[constants.EMAIL]
    post_bio = response_public[constants.DESCRIPTION]
    response_profile = crud.select_all_photo_info_for_user(username, constants.PHOTO_TYPE_PROFILE)

    trans = Translator()
    translate_name = trans.translate(post_username)
    translated_name = translate_name.text
    translate_region = trans.translate(post_region)
    translated_region = translate_region.text
    translate_bio = trans.translate(post_bio)
    translated_bio = translate_bio.text

    profile_location = response_profile[0]
    photo_location = profile_location[constants.PHOTO_LOCATION]
    url_profile = s3.generate_presigned_url('get_object',
                                            Params={
                                                'Bucket': constants.S3_BUCKET_NAME,
                                                'Key': photo_location,

                                            },
                                            ExpiresIn=3600)
    url_list = []
    for index in response_photo:
        location = index[constants.PHOTO_LOCATION]
        url = s3.generate_presigned_url('get_object',
                                        Params={
                                            'Bucket': constants.S3_BUCKET_NAME,
                                            'Key': location,

                                        },
                                        ExpiresIn=3600)
        url_list.append(url)
    print(url_list)

    return render_template('home.html', username=post_username, bio=post_bio, email=post_email, region=post_region,
                           url_list=url_list, url_profile=url_profile, trans_name=translated_name,
                           trans_bio=translated_bio,
                           trans_region=translated_region)


@webapp.route('/recommand', methods=['POST', 'GET'])
def recommand():
    username = session['current_username']
    pword = session['current_password']
    desired_photo = request.files['Desired Photo']
    interested_photo_name = create_filename(desired_photo)
    latitude = None
    longitude = None
    # todo replace with user input
    threshold = 30

    s3.upload_fileobj(desired_photo, constants.S3_BUCKET_NAME, interested_photo_name)

    photo_info = PhotoInfo(username, interested_photo_name, constants.PHOTO_TYPE_INTERESTED, None, None)
    crud.update_photo_info(photo_info)
    public_user_info = crud.select_public_user_info(username)

    potential_interests = ml_util.find_nearby_matching_photo(interested_photo_name,
                                                             public_user_info[constants.GENDER_AND_INTEREST], latitude,
                                                             longitude, threshold)

    potential_interest_urls = []
    for interest in potential_interests:
        url = s3.generate_presigned_url('get_object',
                                        Params={
                                            'Bucket': constants.S3_BUCKET_NAME,
                                            'Key': interest[1],
                                        },
                                        ExpiresIn=3600)
        photo_owner_tuple = (url, interest[0])
        potential_interest_urls.append(photo_owner_tuple)

    # extract the profile photo, user info, history posts
    response_photo = crud.select_all_photo_info_for_user(username, constants.PHOTO_TYPE_POST)
    response_profile = crud.select_all_photo_info_for_user(username, constants.PHOTO_TYPE_PROFILE)

    post_username = public_user_info[constants.USERNAME]
    post_region = public_user_info[constants.REGION]
    post_email = public_user_info[constants.EMAIL]
    post_bio = public_user_info[constants.DESCRIPTION]

    trans = Translator()
    translate_name = trans.translate(post_username)
    translated_name = translate_name.text
    translate_region = trans.translate(post_region)
    translated_region = translate_region.text
    translate_bio = trans.translate(post_bio)
    translated_bio = translate_bio.text

    profile_location = response_profile[0]
    photo_location = profile_location[constants.PHOTO_LOCATION]
    url_profile = s3.generate_presigned_url('get_object',
                                            Params={
                                                'Bucket': constants.S3_BUCKET_NAME,
                                                'Key': photo_location,

                                            },
                                            ExpiresIn=3600)
    url_post_list = []
    for index in response_photo:
        location = index[constants.PHOTO_LOCATION]
        url = s3.generate_presigned_url('get_object',
                                        Params={
                                            'Bucket': constants.S3_BUCKET_NAME,
                                            'Key': location,

                                        },
                                        ExpiresIn=3600)
        url_post_list.append(url)

    return render_template('home.html', matched=potential_interest_urls, username=post_username, bio=post_bio,
                           email=post_email,
                           region=post_region, url_list=url_post_list, url_profile=url_profile,
                           trans_name=translated_name,
                           trans_bio=translated_bio, trans_region=translated_region)
