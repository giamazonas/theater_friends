from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.show import Show

shows = Blueprint('shows', 'shows')

@shows.route('/', methods=["POST"])
@login_required
def create():
  data = request.get_json()
  print(data)
  profile = read_token(request)
  data["profile_id"] = profile["id"]
  show = Show(**data)
  db.session.add(show)
  db.session.commit()
  return jsonify(show.serialize()), 201

@shows.route('/', methods=["GET"])
def index():
  shows = Show.query.all()
  print(shows)
  return jsonify([show.serialize() for show in shows]), 200

@shows.route('/<id>', methods=["GET"])
def show(id):              
  show = Show.query.filter_by(id=id).first()
  show_data = show.serialize()
  return jsonify(show=show_data), 200
# this show in second line, 26, may be problematic 

@shows.route('/<id>', methods=["PUT"]) 
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  show = Show.query.filter_by(id=id).first()

  if show.profile_id != profile["id"]:
    return 'Forbidden', 403

  for key in data:
    setattr(show, key, data[key])

  db.session.commit()
  return jsonify(show.serialize()), 200

@shows.route('/<id>', methods=["DELETE"]) 
@login_required
def delete(id):
  profile = read_token(request)
  show = Show.query.filter_by(id=id).first()

  if show.profile_id != profile["id"]:
    return 'Forbidden', 403

  db.session.delete(show)
  db.session.commit()
  return jsonify(message="Success"), 200

@shows.errorhandler(Exception)          
def basic_error(err):
  return jsonify(err=str(err)), 500

