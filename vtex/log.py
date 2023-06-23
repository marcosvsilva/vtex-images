import os
import json

def log_error(error, sku_id):
    name_file = '{}.json'.format(sku_id)
    if os.path.exists(name_file):
        os.remove(name_file)
    
    data = {"error": error}

    with open(name_file, 'w') as file:
        json.dump(data, file)
    
    print(f'\n   Error: {error}\n')


def log_response(response, sku_id):
    name_file = '{}.json'.format(sku_id)
    if os.path.exists(name_file):
        os.remove(name_file)
    
    if response:
        data = {"status": response.status_code, "body": response.content.decode("utf-8")}

        with open(name_file, "w") as file:
            json.dump(data, file)

    if response.status_code == 200:
        print(f'\n    Product {sku_id} was update successful!')
        print(f'    Response: {response.content}\n\n')
    else:
        print(f'\n    Product {sku_id} update was fail!\n')
        print(f'    Response: {response.content}\n\n')