
from . import app
import os
import json
from flask import jsonify, request

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")

with open(json_url, "r", encoding="utf-8") as file:
    data: list = json.load(file)


######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify(status="OK"), 200


######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    return jsonify(length=len(data)), 200


######################################################################
# GET ALL PICTURES
######################################################################

@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200


######################################################################
# GET A PICTURE BY ID
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200

    return jsonify(message="Picture not found"), 404


######################################################################
# CREATE A PICTURE
######################################################################

@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json(silent=True)

    if not isinstance(picture, dict) or "id" not in picture:
        return jsonify(message="Invalid picture data"), 400

    for existing_picture in data:
        if existing_picture["id"] == picture["id"]:
            return jsonify(
                Message=f"picture with id {picture['id']} already present"
            ), 302

    data.append(picture)

    return jsonify(picture), 201


######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_picture = request.get_json(silent=True)

    if not isinstance(updated_picture, dict):
        return jsonify(message="Invalid picture data"), 400

    for index, picture in enumerate(data):
        if picture["id"] == id:
            updated_picture["id"] = id
            data[index] = updated_picture
            return jsonify(updated_picture), 200

    return jsonify(message="Picture not found"), 404


######################################################################
# DELETE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for index, picture in enumerate(data):
        if picture["id"] == id:
            data.pop(index)
            return "", 204

    return jsonify(message="Picture not found"), 404

