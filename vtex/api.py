import os
import requests
import boto3
import uuid
from config import STORE, ENVIRONMENT, APPKEY, APPTOKEN, S3_BUCKET

base_url = f"https://{STORE}.{ENVIRONMENT}.com.br/api/catalog/pvt/stockkeepingunit"

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
            type_file = path_image.split("/")[-1].split(".")[-1]
            key = 'images/{}.{}'.format(file_id, type_file)
            s3.upload_file(path_image, S3_BUCKET, key)
            s3_public_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"
        except Exception as e:
            print("Error checking file existence:", str(e))

    return s3_public_url

def update_api(input_name, file_path, sku_id, is_main=False):
    if '.png' not in file_path:
        print(r"{file_path}! is not valid .png image.")
        return {}

    if not os.path.exists(file_path):
        print(r"{file_path} not found.")
        return {}
    
    path_upload = upload_image_s3(file_path)
    print(path_upload)

    if path_upload:
        body = {
            'IsMain': is_main,
            'Label': '',
            'Name': input_name,
            'Text': input_name,
            'Url' : path_upload
        }

        headers = {
            'x-vtex-api-appkey': APPKEY,
            'x-vtex-api-apptoken': APPTOKEN,
        }

        url = "{}/{}/file".format(base_url, sku_id)
        response = requests.request("POST", url, headers=headers, json=body)

        if response.status_code == 200:
            print('SUCESS!')
        else:
            print("FAIL")
            print(response.status_code)
            print(response.content)
