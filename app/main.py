from flask import Flask,render_template
from app.app import webapp
@webapp.route('/',methods=['GET'])
def main():
    return render_template("loginpage.html")


