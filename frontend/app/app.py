from flask import Flask
webapp=Flask(__name__)
webapp.static_folder = 'static'