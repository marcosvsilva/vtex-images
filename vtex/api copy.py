import os
import requests
import json
import boto3
import uuid
from config import STORE, ENVIRONMENT, APPKEY, APPTOKEN, S3_BUCKET

base_url = f"https://{STORE}.{ENVIRONMENT}.com.br/api/catalog/pvt/stockkeepingunit"

def upload_image_s3(path_image):
    s3_public_url = ''
    
    if S3_BUCKET != '':
        s3 = boto3.client('s3')
        uuid = uuid.v6()
        try:
            key = 'images/{}'.format(uuid)
            s3.upload_file(path_image, S3_BUCKET, key)
            s3_public_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"
            print("File uploaded successfully.")
        except Exception as e:
            print("Error checking file existence:", str(e))

        print(s3);

    return s3_public_url

def update_api(input_name, file_path, sku_id, is_main=False):
    if '.png' not in file_path:
        print(r"{file_path}! is not valid .png image.")
        return {}

    if not os.path.exists(file_path):
        print(r"{file_path} not found.")
        return {}
    
    path_upload = upload_image_s3(file_path)

    if path_upload:
        file_name = file_path.split('/')[-1]
        files=[('file',(input_name,open(file_path,'rb'),'image/png'))]

        body = {
            'IsMain': is_main,
            'Label': '',
            'Name': input_name,
            'Text': file_name
        }

        headers = {
            'x-vtex-api-appkey': APPKEY,
            'x-vtex-api-apptoken': APPTOKEN,
        }

        url = "{}/{}/file".format(base_url, sku_id)
        print(url)
        response = requests.request("POST", url, headers=headers, files=files)
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.text)

        if response.status_code == 200:
            json_response = json.loads(response.content)
            new_url = "{}/{}".format(url, json_response['ArchiveId'])
            print(new_url)
            print(body)
            update_response = requests.request("PUT", new_url, headers=headers, json=body)
            print("Response Status Code:", response.status_code)
            print("Response Content:", response.text)
            if update_response.status_code == 200:
                print('SUCESS!')
        else:
            print("---------FAIL---------")
            print(response.status_code)
            print(response.content)