import boto3
import os


boto_table = os.environ.get('DB_TABLE', None)

dynamodb = boto3.client('dynamodb')


def getkey(key):
    try:
        return dynamodb.get_item(TableName=boto_table, Key=key)
    except Exception as e:
        return None


def setkey(chat_id, value):
    return dynamodb.put_item(TableName=boto_table, Item=value)


def deletekey(key):
    try:
        return dynamodb.delete_item(TableName=boto_table, Key=key)
    except Exception as e:
        return None


def get_all():
    return dynamodb.scan(TableName=boto_table)
