import json
import re
import copy
import os
import io

import sqlalchemy

from flask import Blueprint, jsonify, request, current_app, Response
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from collections import OrderedDict

crud = Blueprint('crud', __name__)

from model import db, datetime_handler
from auth import login_required


def get_class_by_tablename(table):
    for clss in db.Model._decl_class_registry.values():
        if type(clss) is sqlalchemy.ext.declarative.clsregistry._ModuleMarker:
            continue
        if str.lower(str(clss.__table__)) == str.lower(table):
            return clss


def sort_dict_first_last(obj, first, last):
    obj_dict = copy.deepcopy(obj)
    if obj_dict.get('_sa_instance_state'):
        del(obj_dict['_sa_instance_state'])
    obj_first = OrderedDict()
    obj_last = OrderedDict()
    for k in first:
        if k in obj_dict:
            obj_first.update(OrderedDict({k: obj_dict[k]}))
            del(obj_dict[k])
    for k in last:
        if k in obj_dict:
            obj_last.update(OrderedDict({k: obj_dict[k]}))
            del(obj_dict[k])
    obj_first.update(obj_last)
    return obj_first


def find_relations(any_class, obj_dict, obj):
    related_obj = {}
    clss = get_class_by_tablename(any_class)
    relations = re.findall('([\w\d]*)>', str(sqlalchemy.inspection.inspect(clss).relationships._data))
    for relation in relations:
        relation_name = relation.partition("_back")[0]
        if len(relation) != 0:
            if re.findall('(' + relation.partition("_back")[0] + '_' + any_class + '|' + any_class + '_' + relation.partition("_back")[0] + ')', str(sqlalchemy.inspection.inspect(clss).relationships._data[relation]._calculated_foreign_keys)):
                relation_name = re.findall('(' + relation.partition("_back")[0] + '_' + any_class + '|' + any_class + '_' + relation.partition("_back")
                                           [0] + ')', str(sqlalchemy.inspection.inspect(clss).relationships._data[relation]._calculated_foreign_keys))[0] + '__nton'
                if obj_dict is not None:
                    obj_dict[relation_name.partition("__nton")[0]] = 'nton'
            if obj is not None:
                if getattr(obj, relation) is not None:
                    if isinstance(getattr(obj, relation), list):
                        relation_result = [copy.deepcopy(u.__dict__) for u in getattr(obj, relation)]
                    else:
                        relation_result = [copy.deepcopy(getattr(obj, relation).__dict__)]
                    for rslt in relation_result:
                        if rslt.get('_sa_instance_state'):
                            del(rslt['_sa_instance_state'])
                    related_obj[relation_name] = relation_result  # TODO: Make more flexible
            else:
                related_obj[relation_name] = None
    return related_obj


@crud.route("/api/db_structure", methods=['GET'])
@login_required(False, True)
def get_db_structure():
    obj = {}
    for clss in db.Model._decl_class_registry.values():
        if type(clss) is sqlalchemy.ext.declarative.clsregistry._ModuleMarker:
            continue
        # TODO: Make this more flexible
        order_dict_first = ['image_url', 'name', 'email', 'title', 'content', 'info']
        order_dict_last = ['user_id', 'media_type_id', 'cd_type_id', 'job_type_id',
                           'artist_id', 'media_id', 'role_type_id', 'news_id',
                           'display', 'admin', 'confirmed', 'comment_allowed']
        globals().update(locals())
        tmp_middle = [u.key for u in clss.__table__.columns if u.key not in order_dict_last and u.key not in order_dict_first]
        order_dict_last = tmp_middle + order_dict_last
        obj[clss.__tablename__] = {}
        for col in clss.__table__.columns:
            obj[clss.__tablename__][col.key] = {}
            obj[clss.__tablename__][col.key] = {}
            obj[clss.__tablename__][col.key]["type"] = str(col.type)
            obj[clss.__tablename__][col.key]["nullable"] = str(col.nullable)
        obj[clss.__tablename__] = sort_dict_first_last(obj[clss.__tablename__], order_dict_first, order_dict_last)
        related_obj = find_relations(clss.__tablename__, None, None)
        for rel in related_obj:
            if '__nton' in rel:
                obj[clss.__tablename__][rel.partition("__nton")[0]] = {}
                obj[clss.__tablename__][rel.partition("__nton")[0]]["type"] = 'NTON'
                obj[clss.__tablename__][rel.partition("__nton")[0]]["nullable"] = 'True'
    return Response(response=json.dumps(obj),
                    status=200,
                    mimetype="application/json")


# TODO: optimiser, prends beaucoup trop de temps
@crud.route("/api/get/<any_class>", methods=['GET', 'POST'])
@crud.route("/api/get/<any_class>/<_id>", methods=['GET', 'POST'])
@login_required(False, True)
def get_any_class(any_class, _id=None):
    clss = get_class_by_tablename(any_class)
    if clss is None:
        print("This table doesn't fucking exist")
        return jsonify({'message': "This table doesn't fucking exist"}), 404
    datas = request.get_json()
    if datas is not None:
        filters = datas.get('filter')
    else:
        filters = None
    print(datas)
    print('                  ')
    col = [u.key for u in clss.__table__.columns]
    col = [u.key for u in clss.__table__.columns]
    globals().update(locals())
    if datas:
        if _id is None and filters is not None:
            if filters.get('order_by') is not None:
                if filters.get('order_by').split(" ", 1)[0] not in col:
                    print("Bad order_by Filter")
                    return Response(response=json.dumps({"message": "Bad order_by Filter"}),
                                    status=400,
                                    mimetype="application/json")
            if filters.get('filter_by') is not None:
                if isinstance(filters.get('filter_by'), str):
                    print("Bad filter_by Filter, excepted object, got str")
                    return Response(response=json.dumps({"message": "Bad filter_by Filter, excepted object, got str"}),
                                    status=400,
                                    mimetype="application/json")
    try:
        if _id is not None:
            objects = [clss.query.filter_by(id=_id).first()]
        elif filters is not None and filters.get('filter_by_nton'):
            try:
                objectFilterNton = list(filters['filter_by_nton'])[0]
                itemsFilterNton = filters['filter_by_nton'][objectFilterNton].items()
                clssNton = get_class_by_tablename(objectFilterNton[0:-1])
                objects = clss.query.filter(getattr(clss, objectFilterNton).any(clssNton.title.ilike(dict(itemsFilterNton)['title']))).order_by(filters.get("order_by")).all()
            except AttributeError:
                print("Bad Filter")
                return Response(response=json.dumps({"message": "Bad Filter"}),
                                status=400,
                                mimetype="application/json")

        elif filters is not None and filters.get('filter_by'):
            objects = clss.query.filter_by(**{k: check(v) for k, v in filters.get('filter_by').items() if k in col}).order_by(filters.get("order_by")).all()
        else:
            if filters is not None:
                objects = clss.query.order_by(filters.get("order_by")).all()
            else:
                objects = clss.query.all()
    except sqlalchemy.exc.ProgrammingError:
        print("Wrong Data")
        return Response(response=json.dumps({"message": "Wrong Data"}),
                        status=400,
                        mimetype="application/json")

    if objects is None:
        print("This object doesn't fucking exist")
        return Response(response=json.dumps({"message": "This object doesn't fucking exist"}),
                        status=404,
                        mimetype="application/json")
    if len(objects) == 0:
        print("Empty database for this object")
        return Response(response=json.dumps({"message": "Empty database for this object"}),
                        status=400,
                        mimetype="application/json")
    if objects[0] is None and len(objects) == 1:
        print("Empty database for this object")
        return Response(response=json.dumps({"message": "Empty database for this object"}),
                        status=400,
                        mimetype="application/json")

    # We transform it in an object and we don't take the relationships

    obj_result = []
    obj_dict = {}
    related_obj = {}
    # TODO: Make this more flexible
    order_dict_first = ['image_url', 'name', 'email', 'title', 'content', 'info']
    order_dict_last = ['user_id', 'media_type_id', 'cd_type_id', 'job_type_id',
                       'artist_id', 'media_id', 'role_type_id', 'news_id',
                       'display', 'admin', 'confirmed', 'comment_allowed']

    globals().update(locals())
    tmp_middle = [u.key for u in clss.__table__.columns if u.key not in order_dict_last and u.key not in order_dict_first]
    order_dict_last = tmp_middle + order_dict_last

    for obj in objects:
        obj_dict_partial = {k: v for k, v in obj.__dict__.items() if isinstance(v, list) is not True and k != "_sa_instance_state"}
        obj_dict = sort_dict_first_last(obj_dict_partial, order_dict_first, order_dict_last)
        related_obj = find_relations(any_class, obj_dict, obj)
        obj_result.append({"obj": obj_dict, "rel": related_obj})

    final_result = obj_result
    print(json.dumps(final_result, default=datetime_handler))
    return Response(response=json.dumps(final_result, default=datetime_handler),
                    status=200,
                    mimetype="application/json")


def check(v):
    if isinstance(v, str) is not True:
        return v
    if v.lower() == 'false':
        return False
    elif v.lower() == 'true':
        return True
    else:
        return v


@crud.route("/api/upload/<any_class>/<_id>", methods=['POST'])
def upload_file(any_class, _id):

    try:
        file = request.files['file']
    except KeyError:
        return Response(response=json.dumps({'message': "Bad Request Type"}),
                        status=400,
                        mimetype="application/json")
    filename = secure_filename(file.filename)

    # Gen GUUID File Name
    fileExt = filename.split('.')[-1]

    newFileName = str(any_class) + '_' + str(_id) + request.values['field_name'] + '.' + fileExt
    if 'mp3' in any_class or 'fan' in any_class:
        file.save(os.path.join(os.environ['APP_DIRECTORY'] + '/admin/static/' + any_class, newFileName))
    else:
        file.save(os.path.join(os.environ['APP_DIRECTORY'] + '/admin/static/img/' + any_class, newFileName))
    return Response(response=json.dumps({'message': "File updated"}),
                    status=200,
                    mimetype="application/json")


@crud.route("/api/update/<any_class>", methods=['POST'])
def update_any_class(any_class):
    datas = request.get_json()
    if datas is None:
        print("No data provided for update")
        return Response(response=json.dumps({'message': "No data provided for update"}),
                        status=400,
                        mimetype="application/json")
    print("update", datas)
    clss = get_class_by_tablename(any_class)
    if clss is None:
        print("This table doesn't fucking exist")
        return Response(response=json.dumps({'message': "This table doesn't fucking exist"}),
                        status=400,
                        mimetype="application/json")

    # TODO: Enlever le processing d'image de ce côté.
    # image_data = re.sub('^data:image/.+;base64,', '', datas['file'])
    # photo = FileStorage(io.StringIO(image_data), '{name}.{extension}'.format(name=any_class + str(datas['id']), extension='jpg'))
    # photo = current_app.photos.save(photo, any_class, any_class + str(datas['id']) + '.')
    col = [u.key for u in clss.__table__.columns]
    # This updates the global variables with the local ones to be used in list comprehension
    globals().update(locals())
    # print({k: check(v) for k, v in datas.items() if k in col})
    obj = clss(**{k: check(v) for k, v in datas.items() if k in col})
    # if photo is not None:
    #     obj.image_url = photo
    db.session.merge(obj)
    obj_result = obj.__dict__
    print("update", obj_result)
    del(obj_result['_sa_instance_state'])
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        print("Empty data on NOT NULL fields")
        return Response(response=json.dumps({'message': "Empty data on NOT NULL fields"}),
                        status=400,
                        mimetype="application/json")

    if any_class in ['media', 'artist', 'news']:
        send = obj
        send = send.__dict__
        send['objectID'] = send['id']
        if any_class == "media":
            current_app.indexMedia.add_objects([send])
        if any_class == "news":
            current_app.indexNews.add_objects([send])
        if any_class == "artist":
            current_app.indexArtist.add_objects([send])

    return Response(response=json.dumps(obj_result),
                    status=200,
                    mimetype="application/json")


@crud.route("/api/delete/<any_class>", methods=['POST'])
def delete_any_class(any_class):
    datas = request.get_json()
    print("delete", datas)
    clss = get_class_by_tablename(any_class)
    if clss is None:
        print("This table doesn't fucking exist")
        return Response(response=json.dumps({'message': "This table doesn't fucking exist"}),
                        status=400,
                        mimetype="application/json")
    col = [u.key for u in clss.__table__.columns]
    globals().update(locals())
    obj = clss.query.filter_by(**{k: check(v) for k, v in datas.items() if k in col}).first()
    if obj is None:
        print("No objects to delete")
        return Response(response=json.dumps({'message': "No objects to delete"}),
                        status=400,
                        mimetype="application/json")

    if any_class in ['media', 'artist', 'news']:
        if any_class == "media":
            current_app.indexMedia.delete_object(str(obj.__dict__['id']))
        if any_class == "news":
            current_app.indexNews.delete_object(str(obj.__dict__['id']))
        if any_class == "artist":
            current_app.indexArtist.delete_object(str(obj.__dict__['id']))

    db.session.delete(obj)
    db.session.commit()

    return Response(response=json.dumps({'message': "Object deleted"}),
                    status=200,
                    mimetype="application/json")
