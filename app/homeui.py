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
        if response == None:
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
    Birthday = year + month
    print(Birthday)
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
    s3 = boto3.client('s3')
    full_filename = create_filename(profile_photo)
    s3.upload_fileobj(profile_photo, 'dongxuren1779a2', full_filename)
    public_info = PublicUserInfo(username, email, name, Birthday, Sex, region,
                                 Bio)
    response_public = crud.update_public_user_info(public_info)
    private_info = PrivateUserInfo(username, password, None, None, None)
    response_private = crud.update_private_user_info(private_info)
    photo_infos = PhotoInfo(username, full_filename, constants.PHOTO_TYPE_PROFILE, Sex, None)
    response = crud.update_photo_info(photo_infos)

    return redirect(url_for('load_homepage'))


@webapp.route('/post', methods=['POST', 'GET'])
def post():
    return render_template('post.html')


@webapp.route('/load_homepage', methods=['POST', 'GET'])
def load_homepage():
    # use username to get posted image and user profile
    s3 = boto3.client('s3')
    username = session['current_username']
    response_public = crud.select_public_user_info(username)
    response_photo = crud.select_all_photo_info_for_user(username)
    # todo need modification here
    post_username = response_public[constants.USERNAME]
    post_region = response_public[constants.REGION]
    post_email = response_public[constants.EMAIL]
    post_bio = response_public[constants.DESCRIPTION]
    response_profile = crud.select_profile_photo_info_for_user(username)

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
                           url_list=url_list, url_profile=url_profile)


@webapp.route('/recommand', methods=['POST', 'GET'])
def recommand():
    s3 = boto3.client('s3')
    username = session['current_username']
    pword = session['current_password']
    Desired_photo = request.files['Desired Photo']
    full_filename = create_filename(Desired_photo)

    s3.upload_fileobj(Desired_photo, 'dongxuren1779a2', full_filename)
    url = s3.generate_presigned_url('get_object',
                                    Params={
                                        'Bucket': constants.S3_BUCKET_NAME,
                                        'Key': full_filename,

                                    },
                                    ExpiresIn=3600)
    # sex=session['current_sex']

    photo_info = PhotoInfo(username, full_filename, constants.PHOTO_TYPE_INTERESTED, None, None)
    crud.update_photo_info(photo_info)
    # private_info = PrivateUserInfo(username, pword,photo_infos,{},{})
    # response_private = crud.update_private_user_info(private_info)
    # ml functions below
    response_profile = crud.select_all_profile_photo_info()
    location_list = []
    # this list should include all profile photo location

    for item in response_profile:
        if item[constants.PHOTO_TYPE] == constants.PHOTO_TYPE_PROFILE:
            location = item[constants.PHOTO_LOCATION]
            photo_owner = item[constants.USERNAME]
            owner_location_tuple = (location, photo_owner)
            location_list.append(owner_location_tuple)
    response_matched = ml_util.find_matching_photo(full_filename, location_list)
    print(response_matched)
    # list of urls that match the search
    url_list = []
    for item in response_matched:
        url = s3.generate_presigned_url('get_object',
                                        Params={
                                            'Bucket': constants.S3_BUCKET_NAME,
                                            'Key': item[0],

                                        },
                                        ExpiresIn=3600)
        photo_owner_tuple = (url, item[1])
        url_list.append(photo_owner_tuple)

    # extract the profile photo, user info, history posts
    response_public = crud.select_public_user_info(username)
    response_photo = crud.select_all_photo_info_for_user(username)
    # todo need modification here
    post_username = response_public[constants.USERNAME]
    post_region = response_public[constants.REGION]
    post_email = response_public[constants.EMAIL]
    post_bio = response_public[constants.DESCRIPTION]
    response_profile = crud.select_all_photo_info_for_user(username, constants.PHOTO_TYPE_PROFILE)

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

    return render_template('home.html', matched=url_list, username=post_username, bio=post_bio, email=post_email,
                           region=post_region, url_list=url_post_list, url_profile=url_profile)
