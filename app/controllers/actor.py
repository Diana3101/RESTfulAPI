from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
#from models import Actor, Movie
from settings.constants import ACTOR_FIELDS  # to make response pretty
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_actor_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_actor():
    """
    Add new actor
    """
    ### YOUR CODE HERE ###
    data = get_request_data()
    if 'name' in data.keys():
        if 'date_of_birth' in data.keys():
            if 'gender' in data.keys():
                try:
                    data['date_of_birth'] = dt.strptime(data['date_of_birth'], '%d.%m.%Y').date()
                except:
                    err = 'Wrong data format'
                    return make_response(jsonify(error=err), 400)
                if data['gender'].isalpha():
                    new_record = Actor.create(**data)
                    try:
                        new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
                    except:
                        err = 'Record with such id does not exist'
                        return make_response(jsonify(error=err), 400)

                    return make_response(jsonify(new_actor), 200)
                else:
                    err = 'Wrong gender format'
                    return make_response(jsonify(error=err), 400)
            else:
                err = 'No gender specified'
                return make_response(jsonify(error=err), 400)
        else:
            err = 'No date_of_birth specified'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No name specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    keys = list(data.keys())
    keys.remove('id')
    for i in range(len(keys)):
        if keys[i] == 'date_of_birth':
            try:
                data['date_of_birth'] = dt.strptime(data['date_of_birth'], '%d.%m.%Y').date()
            except:
                err = 'Wrong data format'
                return make_response(jsonify(error=err), 400)
            continue
        elif keys[i] == 'name':
            continue
        elif keys[i] == 'gender':
            continue
        else:
            err = 'Wrong keys'
            return make_response(jsonify(error=err), 400)
    try:
        upd_record = Actor.update(row_id, **data)
        upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
        return make_response(jsonify(upd_actor), 200)
    except:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)




def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
            Actor.delete(row_id)
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
    msg = 'Record successfully deleted'
    return make_response(jsonify(message=msg), 200)


def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()
    if 'id' in data.keys():
        if 'relation_id' in data.keys():
            try:
                actor_id = int(data['id'])
            except:
                err = "actor_id must be an integer"
                return make_response(jsonify(error=err), 400)
            try:
                row_m_id = int(data['relation_id'])
            except:
                err = "movie_id must be integer"
                return make_response(jsonify(error=err), 400)
            movie = Movie.query.filter_by(id=row_m_id).first()
            actor = Actor.add_relation(actor_id, movie)
            try:
                rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            except:
                err = 'Record with such id does not exist'
                return make_response(jsonify(error=err), 400)

            rel_actor['filmography'] = str(actor.filmography)
            return make_response(jsonify(rel_actor), 200)
        else:
            err = 'No relation_id specified'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            actor_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        actor = Actor.clear_relations(actor_id)
        try:
            rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

