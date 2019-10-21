"""VKauth package
"""
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, request, make_response, session
import requests
import vk_api

import sys
print(sys.executable)
print(sys.version)
print(sys.path)


app = Flask(__name__)
code = '1'
VK_APP_ID = '7172984'


@app.route('/')
@app.route('/index')
def index():
    """
    """
    if not request.cookies.get('VKAuth'):
        url = '/login'
        return render_template("index.html", bttnredirect=url)
    else:
        return redirect('/login')


@app.route('/login/')
def login():
    """Redirect to /code with vk code"""
    if not request.cookies.get('VKAuth'):
        login_url = "https://oauth.vk.com/authorize?client_id={0}&scope=friends,offline&redirect_uri=http://0.0.0.0/code&response_type=code".format(
            VK_APP_ID)
        return redirect(login_url)
    else:
        return redirect('/friends_list')


def set_cookies(access_token):
    """Записывает куки, если их еще нет"""
    if not request.cookies.get('VKAuth'):
        res = make_response("Setting a cookie")
        res.set_cookie('VKAuth', value="lol kek", max_age=60*60*24*30)

        print("COOKIES ARE SET")
    else:
        print("THRERE ARE ALREADY COOKIES", request.cookies.get('VKAuth'))


@app.route('/code/')
def get_code():
    global code
    code = request.args.get('code')
    access_token = vk_api.get_access_token(code)
    print("GOT ACCESS TOKEN: ", access_token)
    print("ACCESS_TOKEN_TYPE: ", type(access_token))
    res = redirect('/friends_list')
    res.set_cookie('VKAuth', access_token, max_age=60*60*24*30)
    return res


@app.route('/friends_list/')
def friends_list():
    access_token = request.cookies.get('VKAuth')
    if access_token:
        print("Successful login, ", access_token)
    else:
        print("Some Problem with cookies")

    print("access_token: ", access_token)
    success = vk_api.get_friends_list(access_token)
    print(success)
    return render_template("friends_list.html", result=success, friends=success)
