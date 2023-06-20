import sys
from dotenv import load_dotenv
from api import update_api

load_dotenv()

num_args = len(sys.argv)

def main(args):
    file_name, file_path, sku_id = args

    update_api(file_name, file_path, sku_id, True)

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 3:
        print(r"No arguments provided! Please provide {file_name}, {file_path} and {sku_id}.")
        sys.exit(1)
    main(args)
