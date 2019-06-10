import json
import uuid
import base64

import requests
from authlib.flask.client import OAuth
from flask import Flask, redirect, session, jsonify, request

import repository
import prediction
import time

app = Flask(__name__)
app.config.from_pyfile("app.cfg")
oauth = OAuth(app)


def save_request_token(token):
    repository.add_request_token(session.get("current_user", ""), token)


def fetch_request_token():
    token = repository.get_request_token(session.get("current_user", ""))
    return token


def fetch_flickr_token():
    token = repository.get_token_by_id(session.get("current_user", ""))
    return token


oauth.register(
    name='flickr',
    client_id=app.config['FLICKR_CLIENT_ID'],
    client_secret=app.config['FLICKR_CLIENT_SECRET'],
    request_token_url=app.config['FLICKR_REQUEST_TOKEN_URL'],
    request_token_params=app.config['FLICKR_REQUEST_TOKEN_PARAMS'],
    access_token_url=app.config['FLICKR_ACCESS_TOKEN_URL'],
    access_token_params=app.config['FLICKR_ACCESS_TOKEN_PARAMS'],
    authorize_url=app.config['FLICKR_AUTHORIZE_URL'],
    api_base_url=app.config['FLICKR_API_BASE_URL'],
    client_kwargs=app.config['FLICKR_CLIENT_KWARGS'],
    save_request_token=save_request_token,
    fetch_request_token=fetch_request_token,
    fetch_token=fetch_flickr_token,
)


@app.route("/")
def hello():
    search_photos("contacts", "cat")
    return "A"


@app.route('/addImage', methods=['POST', 'GET'])
def addImage():
    user = request.json['user']
    session["current_user"] = user
    name = request.json['name']
    payload = request.json['file']
    option = request.json['option']
    originalImage = base64.b64decode(payload)
    current_image = prediction.predict(originalImage)
    current_image = [x[1] for x in current_image if x[2] > 0.2]
    t = time.time()
    if option == 'Profile':
        images = get_photos_of_contact("me")
        captioned_images = []
        for image in images:
            captioned_images.append(get_labels(image))
        returned_images = similar_images(current_image, captioned_images)
    elif option == 'Contacts':
        searched_images = []
        for label in current_image:
            searched_images = searched_images + search_photos("contacts", label)
        captioned_images = []
        for image in searched_images:
            captioned_images.append(get_labels(image))
        returned_images = similar_images(current_image, captioned_images)
    else:
        searched_images = []
        for label in current_image:
            searched_images = searched_images + search_photos("all", label)
        captioned_images = []
        print(searched_images)
        for image in searched_images:
            captioned_images.append(get_labels(image))
        returned_images = similar_images(current_image, captioned_images)

    data = {
        "labels": current_image,
        "images": returned_images
    }
    print("Total timp: ", time.time() - t)
    return jsonify(json.dumps(data)), 200, {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
    }


@app.route("/login")
def login():
    user_id = uuid.uuid4()
    user_id = str(user_id)
    session["current_user"] = user_id
    redirect_uri = "http://localhost:5000/authorize"
    return oauth.flickr.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    token = oauth.flickr.authorize_access_token()
    repository.add_token(session.get("current_user", ""), token)
    redirect_url = "http://localhost:4200/login/"
    redirect_url = redirect_url + session.get("current_user", "")
    return redirect(redirect_url)


@app.route('/profile')
def flickr_profile():
    profile = get_profile()
    profile_info = dict()
    iconfarm = profile.get("person", {}).get("iconfarm")
    iconserver = profile.get("person", {}).get("iconserver")
    nsid = profile.get("person", {}).get("nsid")
    name = profile.get("person", {}).get("realname", {}).get("_content", "")
    if int(iconserver) <= 0:
        buddyicon = "https://www.flickr.com/images/buddyicon.gif"
    else:
        buddyicon = "http://farm{}.staticflickr.com/{}/buddyicons/{}.jpg".format(iconfarm,
                                                                                 iconserver,
                                                                                 nsid)
    profile_info["name"] = name
    profile_info["buddyicon"] = buddyicon
    return jsonify(json.dumps(profile_info)), 200, {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
    }


def get_profile():
    request_url = app.config["FLICKR_API_BASE_URL"] + "rest?"
    parameters = dict()
    parameters["method"] = "flickr.people.getInfo"
    parameters["nojsoncallback"] = 1
    parameters["format"] = "json"
    parameters["api_key"] = app.config["FLICKR_CLIENT_ID"]
    parameters["user_id"] = repository.get_token_by_id(session["current_user"]).get("user_nsid", "")
    resp = requests.get(request_url, parameters)
    return resp.json()


def get_contacts():
    api_key = app.config["FLICKR_CLIENT_ID"]
    method = "flickr.contacts.getList"
    response_format = "json"
    request_url = "rest?method={}&api_key={}&format={}&nojsoncallback={}".format(method, api_key, response_format, 1)
    response = oauth.flickr.get(request_url).json()
    contact_list = []
    for contact in response.get("contacts", {}).get("contact", []):
        contact_list.append(contact.get("nsid", ""))
    return contact_list


def get_photos_of_contact(contact):
    api_key = app.config["FLICKR_CLIENT_ID"]
    method = "flickr.people.getPhotos"
    response_format = "json"
    request_url = "rest?method={}&api_key={}&user_id={}&format={}&nojsoncallback={}".format(method, api_key, contact,
                                                                                            response_format, 1)
    response = oauth.flickr.get(request_url).json()
    photo_list = []
    for photo in response.get("photos", {}).get("photo", []):
        photo_list.append(photo_to_url(photo))
    return photo_list


def search_photos(mode, text):
    api_key = app.config["FLICKR_CLIENT_ID"]
    method = "flickr.photos.search"
    media = "photos"
    sort = "relevance"
    response_format = "json"
    if mode == "me":
        request_url = "rest?method={}&api_key={}&format={}&nojsoncallback={}" \
                      "&text={}&user_id={}&media={}&sort={}".format(method,
                                                                    api_key,
                                                                    response_format,
                                                                    1,
                                                                    text,
                                                                    mode,
                                                                    media,
                                                                    sort)
    elif mode == "contacts":
        request_url = "rest?method={}&api_key={}&format={}&nojsoncallback={}" \
                      "&text={}&contacts={}&media={}&sort={}".format(method,
                                                                     api_key,
                                                                     response_format,
                                                                     1,
                                                                     text,
                                                                     "all",
                                                                     media,
                                                                     sort)
    else:
        request_url = "rest?method={}&api_key={}&format={}&nojsoncallback={}" \
                      "&text={}&media={}&sort={}".format(method,
                                                         api_key,
                                                         response_format,
                                                         1,
                                                         text,
                                                         media,
                                                         sort)
    response = oauth.flickr.get(request_url).json()
    photo_list = []
    for photo in response.get("photos", {}).get("photo", []):
        photo_list.append(photo_to_url(photo))
    print(len(photo_list))
    return photo_list


def photo_to_url(photo):
    data = dict()
    data["farm-id"] = photo.get("farm", "")
    data["server-id"] = photo.get("server")
    data["id"] = photo.get("id")
    data["secret"] = photo.get("secret")
    photo_url = "https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg".format(**data)
    return photo_url


def get_labels(image):
    response = requests.get(image)
    response = response.content
    labels = prediction.predict(response)
    labels = [x[1] for x in labels if x[2] > 0.2]
    return (image, labels)


def similar_images(current_image, image_list):
    similar_images = set()
    for image, labels in image_list:
        print(labels)
        for i in range(0, len(current_image)):
            if current_image[i] in labels:
                similar_images.add(image)
    return list(similar_images)


if __name__ == "__main__":
    app.run(debug=True)
