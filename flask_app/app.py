import os
import uuid
import json
import boto3
from boto3.dynamodb.conditions import Key

from flask import make_response, request, jsonify
from flask_lambda import FlaskLambda


os.environ['EXEC_ENV'] = 'local'
os.environ['REGION_NAME'] = 'us-east-1'
os.environ['TABLE_NAME'] = 'students'

EXEC_ENV = os.environ['EXEC_ENV']
REGION = os.environ['REGION_NAME']
TABLE_NAME = os.environ['TABLE_NAME']

app = FlaskLambda(__name__)

if EXEC_ENV == 'local':
    print('------Configuring local dynamodb access with table name=>', TABLE_NAME)
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb:8000')
else:
    dynamodb = boto3.resource('dynamodb', region_name=REGION)


def table(table_name=TABLE_NAME):
    return dynamodb.Table(table_name)


def parse_user_id(req):
    '''When frontend is built and integrated with an AWS Cognito
       this will parse and decode token to get user identification'''
    return req.headers['Authorization'].split()[1]


@app.route('/')
def index():
    return jsonify( message="Hello, world!")


@app.route('/students', methods=['GET', 'POST'])
def put_list_students():
    if request.method == 'GET':
        students = table.scan()['Items']
        return json_response(students)
    else:
        table.put_item(Item=request.form.to_dict())
        return json_response({"message": "student entry created"})


@app.route('/students/<id>', methods=['GET', 'PATCH', 'DELETE'])
def get_patch_delete_student(id):
    key = {'id': id}
    if request.method == 'GET':
        student = table.get_item(Key=key).get('Item')
        if student:
            return json_response(student)
        else:
            return json_response({"message": "student not found"}, 404)
    elif request.method == 'PATCH':
        attribute_updates = {key: {'Value': value, 'Action': 'PUT'}
                             for key, value in request.form.items()}
        table.update_item(Key=key, AttributeUpdates=attribute_updates)
        return json_response({"message": "student entry updated"})
    else:
        table.delete_item(Key=key)
        return json_response({"message": "student entry deleted"})


def json_response(data, response_code=200):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}
