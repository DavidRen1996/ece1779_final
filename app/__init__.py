from flask import Flask
webapp=Flask(__name__)
webapp.static_folder = 'static'
from flask import Flask,render_template,redirect,url_for,request,g
from app import main
from app import homeui
from app import post
from app import browse
from app import edit_profile_photo


webapp.secret_key = 'Is\xf6\x94X\x8d\xab\x7at\x0fj_q`\xa4\x16\xdbk\x82\x98P\x18\xe6\xe5$\x86\xf9\xd4\xf3Q\x83-\x8c\xea\xa5\xbc\xe0m1\x85\xc2;\xe8\x1c\xe6\xa1\xce\xcd\xab\xbau\x88\x95\x82\x15\x9d\x1ew\x9a8\x86\x14\xcb\x80'
