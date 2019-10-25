"""VKauth package
"""
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, request, session
import vk_api

import sys
print(sys.executable)
print(sys.version)
print(sys.path)


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    """ Render main page if not authorized
        And redirect to page with list of friends if authorized
    """
    if 'access_token' not in session:
        url = '/login'
        return render_template("index.html", bttnredirect=url)
    else:
        return redirect('/friends_list')


@app.route('/login/')
def login():
    """ VK Auth and redirect to /set_cookies with vk code """
    login_url = vk_api.get_login_url()
    return redirect(login_url)


@app.route('/set_cookies')
def set_cookies():
    """ Get access token and set the cookie with it """
    global code
    code = request.args.get('code')
    access_token, user_id = vk_api.get_access_token(code)
    print("GOT ACCESS TOKEN: ", access_token)
    print("ACCESS_TOKEN_TYPE: ", type(access_token))
    print("GOT USER ID: ", user_id)

    session['access_token'] = access_token
    session['user_id'] = user_id

    res = redirect('/friends_list')
    return res


@app.route('/friends_list/')
def friends_list():
    """ Get access_token from the cookie, get user info and friends list using
        VK API and generate page with list of friends
    """
    access_token = session['access_token']
    user_id = session['user_id']

    print("access_token: ", access_token)
    user = vk_api.get_user_data(access_token, user_id)[0]
    friends_list = vk_api.get_friends_list(access_token)
    print(friends_list)
    return render_template("friends_list.html", user_res=user, user=user,
                           result=friends_list, friends=friends_list)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True, host="0.0.0.0", port="80")
