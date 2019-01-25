import json
import datetime
import re

import sqlalchemy

from model import *


#
#   TO TEST :
#   - File upload
#   - Bon ordre lors du order_by
#   - Bon ordre des champs


def test_get_database_struct(app):
    response = app.client.get('/api/db_structure')
    data = json.loads(response.data.decode())
    print(data)
    for clss in db.Model._decl_class_registry.values():
        if type(clss) is sqlalchemy.ext.declarative.clsregistry._ModuleMarker:
            continue
        assert data[clss.__tablename__] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


#
#   Unexisting Table
#

def test_get_unexisting_table(app):
    response = app.client.get('/api/get/eeeee')
    data = json.loads(response.data.decode())
    assert data['message'] == "This object doesn't fucking exist"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_unexisting_table(app):
    response = app.client.post('/api/get/eeeee')
    data = json.loads(response.data.decode())
    assert data['message'] == "This object doesn't fucking exist"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_orderby_unexisting_table(app):
    jsonArray = {}
    jsonArray['order_by'] = "date desc"
    response = app.client.post('/api/get/eeeee',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "This object doesn't fucking exist"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_unexisting_table(app):
    jsonArray = {}
    jsonArray['filter_by_nton'] = {"artists": {"title": "Hans Zimmer"}}
    response = app.client.post('/api/get/eeeee',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "This object doesn't fucking exist"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_unexisting_table(app):
    jsonArray = {}
    jsonArray['filter_by_nton'] = {"artists": {"title": "Hans Zimmer"}}
    jsonArray['order_by'] = "date desc"
    response = app.client.post('/api/get/eeeee',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "This object doesn't fucking exist"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_update_unexisting_table(app):
    response = app.client.post('/api/get/eeeee')
    data = json.loads(response.data.decode())
    assert data['message'] == "This object doesn't fucking exist"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_update_unexisting_table_data(app):
    jsonArray = {"title": "Best Title"}
    response = app.client.post('/api/get/eeeee',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "This object doesn't fucking exist"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_delete_unexisting_table(app):
    response = app.client.post('/api/get/eeeee')
    data = json.loads(response.data.decode())
    assert data['message'] == "This object doesn't fucking exist"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_delete_unexisting_table_data(app):
    jsonArray = {"title": "Best Title"}
    response = app.client.post('/api/get/eeeee',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "This object doesn't fucking exist"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


#
#   Empty Table
#

def test_get_empty_table(app):
    response = app.client.get('/api/get/fan_rate')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF FAN_RATE IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_empty_table(app):
    response = app.client.post('/api/get/fan_rate')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF FAN_RATE IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_orderby_empty_table(app):
    jsonArray = {}
    jsonArray['order_by'] = "rate desc"
    response = app.client.post('/api/get/fan_rate',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️  ----- SHOULD WORK -----")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_orderby_empty_table_unexisting_data(app):
    jsonArray = {}
    jsonArray['order_by'] = "title desc"
    response = app.client.post('/api/get/fan_rate',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF FAN_RATE IS FILLED")
    assert data['message'] == "Bad order_by Filter"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_empty_table(app):
    jsonArray = {}
    jsonArray['filter_by'] = {"rate": 1}
    response = app.client.post('/api/get/fan_rate',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF FAN_RATE IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_empty_table_unexisting_data(app):
    jsonArray = {}
    jsonArray['filter_by'] = {"title": "Hans Zimmer"}
    response = app.client.post('/api/get/fan_rate',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF FAN_RATE IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_empty_table_wrong_nton(app):
    jsonArray = {}
    jsonArray['filter_by_nton'] = {"artists": {"title": "Hans Zimmer"}}
    response = app.client.post('/api/get/fan_rate',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF FAN_RATE IS FILLED")
    assert data['message'] == "Bad Filter"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_empty_table_wrong_data_wrong_nton(app):
    jsonArray = {}
    jsonArray['filter_by_nton'] = {"artists": {"rate": "Hans Zimmer"}}
    response = app.client.post('/api/get/fan_rate',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF FAN_RATE IS FILLED")
    assert data['message'] == "Bad Filter"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_empty_table(app):
    jsonArray = {}
    jsonArray['order_by'] = "rate desc"
    jsonArray['filter_by'] = {"rate": 1}
    response = app.client.post('/api/get/fan_rate',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️  ---- SHOULD WORK -----")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_empty_table_unexisting_data(app):
    jsonArray = {}
    jsonArray['order_by'] = "title desc"
    jsonArray['filter_by'] = {"title": 1}
    response = app.client.post('/api/get/fan_rate',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF FAN_RATE IS FILLED")
    assert data['message'] == "Bad order_by Filter"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_empty_table_wrong_data(app):
    jsonArray = {}
    jsonArray['order_by'] = "title desc"
    jsonArray['filter_by'] = {"artists": {"title": "Hans Zimmer"}}
    response = app.client.post('/api/get/fan_rate',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "Bad order_by Filter"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_update_empty_table(app):
    jsonArray = {"id": 1, "rate": 1}
    response = app.client.post('/api/get/fan_rate',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF FAN_RATE IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_update_empty_table_not_enough(app):
    jsonArray = {"id": 1}
    response = app.client.post('/api/get/fan_rate',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF FAN_RATE IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_delete_post_empty_table(app):
    jsonArray = {"id": 1}
    response = app.client.post('/api/get/fan_rate',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF FAN_RATE IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


#
#   Existing Table
#

#       Unexisting Object

def test_get_post_wrong_json_unexisting_object(app):
    jsonArray = {"id": 1}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_unexisting_object(app):
    response = app.client.get('/api/get/media/1')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_unexisting_object(app):
    jsonArray = {"filter_by": {"id": 1}}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_unexisting_object_wrong_data(app):
    jsonArray = {"filter_by": {"title": 1}}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Wrong Data"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_unexisting_object_wrong_nton_data(app):
    jsonArray = {"filter_by": {"artists": {"rate": "Hans Zimmer"}}}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_unexisting_object_nton(app):
    jsonArray = {"filter_by_nton": {"artists": {"title": "eer"}}}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_unexisting_object_nton_wrong_data(app):
    jsonArray = {"filter_by_nton": {"artists": {"rate": "Hans Zimmer"}}}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Bad Filter"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_unexisting_object_wrong_nton_right_data(app):
    jsonArray = {"filter_by_nton": {"media": {"title": "Hans Zimmer"}}}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Bad Filter"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_unexisting_object_wrong_nton_wrong_data(app):
    jsonArray = {"filter_by_nton": {"media": {"rate": "Hans Zimmer"}}}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Bad Filter"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_table_unexisting_object(app):
    jsonArray = {}
    jsonArray['order_by'] = "title desc"
    jsonArray['filter_by'] = {"id": 1}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️  -------------- NOT NORMAL -----------------")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_table_unexisting_object_nton_filter_by(app):
    jsonArray = {}
    jsonArray['order_by'] = "title desc"
    jsonArray['filter_by_nton'] = {"artists": {"title": "Hans Zimmer"}}
    jsonArray['filter_by'] = {"id": 1}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_table_unexisting_object_unexisting_nton(app):
    jsonArray = {}
    jsonArray['order_by'] = "title desc"
    jsonArray['filter_by_nton'] = {"artists": {"title": "elkrf"}}
    jsonArray['filter_by'] = {"id": 1}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_table_unexisting_object_wrong_nton(app):
    jsonArray = {}
    jsonArray['order_by'] = "title desc"
    jsonArray['filter_by_nton'] = {"media": {"rate": "Hans Zimmer"}}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Bad Filter"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_table_unexisting_object_wrong_order(app):
    jsonArray = {}
    jsonArray['order_by'] = "rate desc"
    jsonArray['filter_by'] = {"id": 1}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Bad order_by Filter"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_table_unexisting_object_wrong_order_nton(app):
    jsonArray = {}
    jsonArray['order_by'] = "rate desc"
    jsonArray['filter_by_nton'] = {"id": 1}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Bad order_by Filter"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_unexisting_object_from_url(app):
    jsonArray = {"filter_by": {"id": 1}}
    response = app.client.post('/api/get/media/1',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_unexisting_object_from_url_wrong_data(app):
    jsonArray = {"filter_by": {"title": 1}}
    response = app.client.post('/api/get/media/1',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_unexisting_object_from_url_wrong_nton_data(app):
    jsonArray = {"filter_by": {"artist": {"title": "Hans Zimmer"}}}
    response = app.client.post('/api/get/media/1',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_unexisting_object_from_url_nton(app):
    jsonArray = {"filter_by_nton": {"artist": {"title": "Hans Zimmer"}}}
    response = app.client.post('/api/get/media/1',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_unexisting_object_from_url_nton_wrong_data(app):
    jsonArray = {"filter_by_nton": {"artist": {"rate": "Hans Zimmer"}}}
    response = app.client.post('/api/get/media/1',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_unexisting_object_from_url_wrong_nton_right_data(app):
    jsonArray = {"filter_by_nton": {"media": {"title": "Hans Zimmer"}}}
    response = app.client.post('/api/get/media/1',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_unexisting_object_from_url_wrong_nton_wrong_data(app):
    jsonArray = {"filter_by_nton": {"media": {"rate": "Hans Zimmer"}}}
    response = app.client.post('/api/get/media/1',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_table_unexisting_object_from_url(app):
    jsonArray = {}
    jsonArray['order_by'] = "title desc"
    jsonArray['filter_by'] = {"id": 1}
    response = app.client.post('/api/get/media/1',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_table_unexisting_object_from_url_with_nton(app):
    jsonArray = {}
    jsonArray['order_by'] = "title desc"
    jsonArray['filter_by_nton'] = {"medias": {"title": "Hans Zimmer"}}
    response = app.client.post('/api/get/media/1',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_table_unexisting_object_from_url_with_wrong_nton(app):
    jsonArray = {}
    jsonArray['order_by'] = "title desc"
    jsonArray['filter_by_nton'] = {"medias": {"rate": "Hans Zimmer"}}
    response = app.client.post('/api/get/media/1',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_table_unexisting_object_from_url_with_wrong_order_data(app):
    jsonArray = {}
    jsonArray['order_by'] = "rate desc"
    jsonArray['filter_by'] = {"id": 1}
    response = app.client.post('/api/get/media/1',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_table_unexisting_object_from_url_with_wrong_order_data_with_nton(app):
    jsonArray = {}
    jsonArray['order_by'] = "rate desc"
    jsonArray['filter_by_nton'] = {"id": 1}
    response = app.client.post('/api/get/media/1',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_update_table_unexisting_object_not_enough(app):
    jsonArray = {"id": 1}
    response = app.client.post('/api/update/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty data on NOT NULL fields"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_update_table_unexisting_object_create(app):
    jsonArray = {"id": 1, "title": "test", "date": "10-10-2018", "content": "tester",
                 "image_url": "test", "length": 123, "label": "testlabel", "tracklist": "testTrack",
                 "amazon": "testamazon", "display": True, "media_type_id": 1, "cd_type_id": 1}
    response = app.client.post('/api/update/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())

    jsonArray = {k: str(v).lower() for k, v in jsonArray.items()}
    data = {k: str(v).lower() for k, v in data.items()}
    assert data == jsonArray
    assert data is not None
    assert data.get('message') is None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_update_table_unexisting_object_update(app):
    jsonArray = {"id": 1, "title": "tester", "date": "12-10-2018", "content": "testerr",
                 "image_url": "tst", "length": 12, "label": "testlbel", "tracklist": "testTack",
                 "amazon": "testmazon", "display": False, "media_type_id": 1, "cd_type_id": 1}
    response = app.client.post('/api/update/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    jsonArray = {k: str(v).lower() for k, v in jsonArray.items()}
    data = {k: str(v).lower() for k, v in data.items()}
    assert data == jsonArray
    assert data is not None
    assert data.get('message') is None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_update_table_unexisting_object_delete(app):
    jsonArray = {"id": 1, "title": "tester", "date": "12-10-2018", "content": "testerr",
                 "image_url": "tst", "length": 12, "label": "testlbel", "tracklist": "testTack",
                 "amazon": "testmazon", "display": False, "media_type_id": 1, "cd_type_id": 1}
    response = app.client.post('/api/delete/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Object deleted"
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_delete_table_unexisting_object(app):
    jsonArray = {"id": 2}
    response = app.client.post('/api/get/fan_rate',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print("⚠️ NORMAL TO FAIL IF MEDIA 1 IS FILLED")
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


#       Existing Object

def test_get_table(app):
    response = app.client.get('/api/get/media')
    data = json.loads(response.data.decode())
    print(data)

    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_get_table_form_url(app):
    response = app.client.get('/api/get/media/6')
    data = json.loads(response.data.decode())
    print(data)

    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_get_post_table(app):
    response = app.client.post('/api/get/media')
    data = json.loads(response.data.decode())
    print(data)

    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_get_post_table_from_url(app):
    response = app.client.post('/api/get/media/6')
    data = json.loads(response.data.decode())
    print(data)

    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_get_post_orderby_table(app):
    jsonArray = {"order_by": "title desc"}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    # TODO: Tester que c'est le bon ordre

    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    if len(data) > 1:
        assert data[0]['title'] < data[0]['title']
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_get_post_orderby_table(app):
    jsonArray = {"order_by": "title desc"}
    response = app.client.post('/api/get/media/6',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    # TODO: Tester que c'est le bon ordre

    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_get_post_orderby_table_not_existing_order(app):
    jsonArray = {"order_by": "rate desc"}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "Bad order_by Filter"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_orderby_table_not_existing_order_empty(app):
    jsonArray = {"order_by": ""}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "Bad order_by Filter"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_orderby_table_not_existing_order_from_url(app):
    jsonArray = {"order_by": "rate desc"}
    response = app.client.post('/api/get/media/6',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_orderby_table_not_existing_order_empty_from_url(app):
    jsonArray = {"order_by": ""}
    response = app.client.post('/api/get/media/6',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table(app):
    jsonArray = {"filter_by": {"title": "inception"}}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_get_post_filterby_table_with_nton(app):
    jsonArray = {"filter_by_nton": {"artists": {"title": "Hans Zimmer"}}}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_get_post_filterby_table_with_nton_wrong_data(app):
    jsonArray = {"filter_by": {"rate": 1}}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_wrong_nton_data(app):
    jsonArray = {"filter_by_nton": {"artists": {"rate": "Hans Zimmer"}}}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "Bad Filter"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_wrong_nton_wrong_data(app):
    jsonArray = {"filter_by_nton": {"medias": {"rate": "Hans Zimmer"}}}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "Bad Filter"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_empty_nton_data(app):
    jsonArray = {"filter_by_nton": {"artists": {"title": "erfpe"}}}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "Empty database for this object"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_empty_nton_empty_data(app):
    jsonArray = {"filter_by_nton": ""}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_empty_data(app):
    jsonArray = {"filter_by": ""}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_from_url_(app):
    jsonArray = {"filter_by": {"title": "inception"}}
    response = app.client.post('/api/get/media/6',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_get_post_filterby_table_from_url_with_nton(app):
    jsonArray = {"filter_by_nton": {"artists": {"title": "Hans Zimmer"}}}
    response = app.client.post('/api/get/media/6',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_get_post_filterby_table_from_url_wrong_data(app):
    jsonArray = {"filter_by": {"rate": 1}}
    response = app.client.post('/api/get/media/6',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_from_url_wrong_nton_data(app):
    jsonArray = {"filter_by_nton": {"artists": {"rate": "Hans Zimmer"}}}
    response = app.client.post('/api/get/media/6',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_from_url_double_wrong_nton_data(app):
    jsonArray = {"filter_by_nton": {"medias": {"rate": "Hans Zimmer"}}}
    response = app.client.post('/api/get/media/6',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_from_url_empty_nton_data(app):
    jsonArray = {"filter_by_nton": {"artists": {"title": "erfpe"}}}
    response = app.client.post('/api/get/media/6',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_from_url__not_empty_data(app):
    jsonArray = {"filter_by_nton": ""}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())

    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_table_from_url_empty_data(app):
    jsonArray = {"filter_by": ""}
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 400


def test_get_post_filterby_orderby_table_nton(app):
    jsonArray = {}
    jsonArray['filter_by_nton'] = {"artists": {"title": "Hans Zimmer"}}
    jsonArray['order_by'] = "title desc"
    response = app.client.post('/api/get/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    print(data)

    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_get_post_filterby_orderby_table_from_url_nton(app):
    jsonArray = {}
    jsonArray['filter_by_nton'] = {"artists": {"title": "Hans Zimmer"}}
    jsonArray['order_by'] = "title desc"
    response = app.client.post('/api/get/media/6',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())

    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_get_post_filterby_orderby_table_from_url_no_nton(app):
    jsonArray = {}
    jsonArray['filter_by'] = {"title": "inception"}
    jsonArray['order_by'] = "title desc"
    response = app.client.post('/api/get/media/6',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())

    assert isinstance(data, list)
    if isinstance(data, list):
        for obj in data:
            assert obj['obj'] is not None
            assert obj['rel'] is not None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_update_table(app):
    jsonArray = {"title": "inceptions"}
    response = app.client.post('/api/update/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "Empty data on NOT NULL fields"
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_update_table_empty_title(app):
    jsonArray = {"title": ""}
    response = app.client.post('/api/update/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "Empty data on NOT NULL fields"
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_update_table_unexisting_field(app):
    jsonArray = {"rate": 1}
    response = app.client.post('/api/update/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "Empty data on NOT NULL fields"
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_update_table_from_with_id(app):
    jsonArray = {"id": 6, "title": "inception"}
    response = app.client.post('/api/update/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())

    assert data['id'] == jsonArray['id']
    assert data['title'] == jsonArray['title'].lower()
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_update_table_with_id_empty_title(app):
    jsonArray = {"id": 6, "title": ""}
    response = app.client.post('/api/update/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())

    assert data['id'] == 6
    assert data['title'] == ""
    assert response.content_type == 'application/json'
    assert response.status_code, 200

    # Redo
    jsonArray = {"id": 6, "title": "inception"}
    response = app.client.post('/api/update/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())

    assert data['id'] == 6
    assert data['title'] == "inception"
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_update_table_with_id__unexisting_field(app):
    jsonArray = {"id": 6, "rate": 1}
    response = app.client.post('/api/update/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())

    assert data['id'] == 6
    assert data.get('rate') is None
    assert response.content_type == 'application/json'
    assert response.status_code, 200


def test_delete_post_filterby_orderby_table(app):
    jsonArray = {"title": "test"}
    response = app.client.post('/api/delete/media',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "No objects to delete"
    assert response.content_type == 'application/json'
    assert response.status_code, 200


#
#   Empty Table
#


def test_file_upload_empty(app):
    jsonArray = {}
    response = app.client.post('/api/upload/media/1',
                               data=json.dumps(jsonArray),
                               content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['message'] == "Bad Request Type"
    assert response.content_type == 'application/json'
    assert response.status_code, 400


#
#
#
# def test_registered_user_password_reset(app):
#     user = User.query.filter(User.email.contains('test'), User.confirmed == True).first()
#     assert user is not None
#     response = app.client.post(
#         '/api/password_reset',
#         data=json.dumps(dict(
#             email=user.email
#         )),
#         content_type='application/json'
#     )
#     data = json.loads(response.data.decode())
#     token = data['token']
#     assert token != ''
#     assert data['message'] == 'We sent you an email to set your password.'
#     assert response.content_type == 'application/json'
#     assert response.status_code, 200

#     response = app.client.post(
#         '/api/confirm/' + token,
#         data=json.dumps(dict(
#             password='test'
#         )),
#         content_type='application/json'
#     )
#     data = json.loads(response.data.decode())
#     assert data['message'] == 'Everything is registered and confirmed.'
#     assert response.content_type == 'application/json'
#     assert response.status_code, 200


# def test_unconfirmed_user_password_reset(app):
#     user = User.query.filter(User.email.contains('test'), User.confirmed == False).first()
#     assert user is not None
#     response = app.client.post(
#         '/api/password_reset',
#         data=json.dumps(dict(
#             email=user.email
#         )),
#         content_type='application/json'
#     )
#     data = json.loads(response.data.decode())
#     token = data['token']
#     assert token != ''
#     assert data['message'] == 'We sent you an email to set your password.'
#     assert response.content_type == 'application/json'
#     assert response.status_code, 200

#     response = app.client.post(
#         '/api/confirm/' + token,
#         data=json.dumps(dict(
#             password='test'
#         )),
#         content_type='application/json'
#     )
#     data = json.loads(response.data.decode())
#     assert data['message'] == 'Everything is registered and confirmed.'
#     assert response.content_type == 'application/json'
#     assert response.status_code, 200


# def test_unregistered_user_password_reset(app):
#     response = app.client.post(
#         '/api/password_reset',
#         data=json.dumps(dict(
#             email='neverexist@neverexist.neverexist'
#         )),
#         content_type='application/json'
#     )
#     data = json.loads(response.data.decode())
#     assert data['message'] == 'There\'s no account with this email address.'
#     assert response.content_type == 'application/json'
#     assert response.status_code, 400
