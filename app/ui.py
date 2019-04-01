from flask import Flask,render_template
from app.app import webapp
@webapp.route('/ui',methods=['GET'])
def ui():
    return render_template("post.html")


