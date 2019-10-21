"""
"""
import requests


def get_access_token(code):
    access_token_link = "https://oauth.vk.com/access_token?client_id=7172984&client_secret=Yz2vR5uLmcOGjJRyUg5H&redirect_uri=http://0.0.0.0/code&code={0}".format(
        code)
    print("code: ", code)
    data = requests.get(url=access_token_link).json()
    print(data)
    access_token = data['access_token']
    user_id = data['user_id']
    return access_token


def get_user_data(access_token, user_ids):
    test_request = "https://api.vk.com/method/users.get?&v=5.102&access_token={0}&user_ids={1}".format(
        access_token, user_ids)
    data = requests.get(url=test_request).json()
    data = data['response']
    return data


def get_friends_list(access_token):
    request_link = "https://api.vk.com/method/friends.get?count=5&aorder=random&v=5.102&access_token={0}".format(
        access_token)
    data = requests.get(url=request_link).json()
    print(data)

    friends_ids = data['response']['items']
    friends_ids_str = str(friends_ids[0])
    for i in friends_ids[1:]:
        friends_ids_str += ","+str(i)
    print(friends_ids_str)

    friends_amount = data['response']['count']
    friends_list = get_user_data(access_token, friends_ids_str)
    return friends_list
