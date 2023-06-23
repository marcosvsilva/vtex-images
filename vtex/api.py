import os
import requests
import boto3
import uuid
from config import STORE, ENVIRONMENT, APPKEY, APPTOKEN, S3_BUCKET
from messages import show_command_not_valid, show_env_not_valid, show_params_not_valid
from log import log_error, log_response

BASE_URL = f"https://{STORE}.{ENVIRONMENT}.com.br/api/catalog/pvt/stockkeepingunit"

SKU_ID = ''

def generate_uuidv6():
    version = 6
    uuidv6 = uuid.uuid4()

    uuidv6_int = int(uuidv6.hex, 16)
    uuidv6_int &= ~(0xf000)
    uuidv6_int |= (version << 12)

    uuidv6_modified = uuid.UUID(int=uuidv6_int)

    return str(uuidv6_modified)

def upload_image_s3(path_image):
    s3_public_url = ''
    
    if S3_BUCKET != '':
        s3 = boto3.client('s3')
        file_id = generate_uuidv6()
        try:
            type_file = os.path.basename(path_image).split(".")[-1]
            key = 'images/{}.{}'.format(file_id, type_file)
            s3.upload_file(path_image, S3_BUCKET, key)
            s3_public_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"
        except Exception as e:
            log_error('Error: checking file existence: ' + str(e), SKU_ID)

    return s3_public_url

def insert_update_api(args, update=False, is_main=True):
    try:
        path_file = args[1]
    except IndexError:
        log_error('Invalid arguments [PATH_FILE] of insert.', SKU_ID)
        return
    
    if not os.path.exists(path_file):
        log_error(f'File {path_file} not found.', SKU_ID)
        return

    if update:
        try:
            file_id = args[2]
        except IndexError:
            log_error('Invalid arguments [FILE_ID] of update.', SKU_ID)
            return
    
    path_upload = upload_image_s3(path_file)
    if not path_upload:
        log_error('Fail to upload image to S3 bucket.', SKU_ID)

    file_name = os.path.basename(path_file).split(".")[0]
    body = {
        'IsMain': is_main,
        'Label': '',
        'Name': file_name,
        'Text': file_name,
        'Url' : path_upload
    }

    headers = {
        'x-vtex-api-appkey': APPKEY,
        'x-vtex-api-apptoken': APPTOKEN,
    }
    
    if not update:
        url = "{}/{}/file".format(BASE_URL, SKU_ID)
        response = requests.request("POST", url, headers=headers, json=body)
        log_response(response, SKU_ID)
    else:
        url = "{}/{}/file/{}".format(BASE_URL, SKU_ID, file_id)
        response = requests.request("PUT", url, headers=headers, json=body)
        log_response(response, SKU_ID)

def delete_api(args):
    try:
        file_id = args[1]
    except IndexError:
        log_error('Invalid arguments [FILE_ID] of delete.', SKU_ID)
        return
    
    headers = {
        'x-vtex-api-appkey': APPKEY,
        'x-vtex-api-apptoken': APPTOKEN,
    }
    
    url = "{}/{}/file/{}".format(BASE_URL, SKU_ID, file_id)
    response = requests.request("DELETE", url, headers=headers)
    log_response(response, SKU_ID)

def run(action, args):
    if "" in [STORE, ENVIRONMENT, APPKEY, APPTOKEN, S3_BUCKET]:
        show_env_not_valid()
        return 0
    
    global SKU_ID
    try:
        SKU_ID = args[0]
    except IndexError:
        show_params_not_valid(action)
        return

    if action == 'i':
        insert_update_api(args)
    elif action == 'u':
        insert_update_api(args, update=True)
    elif action == 'd':
        delete_api(args)
    else:
        show_command_not_valid(action)
