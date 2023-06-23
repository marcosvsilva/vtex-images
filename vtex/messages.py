m_args_insert = '-i [SKU_ID] [PATH_FILE]            path of new image and id of product catalog to upload image'
m_args_update = '-u [SKU_ID] [PATH_FILE] [FILE_ID]  path of new image and id of product catalog to update image'
m_args_delete = '-d [SKU_ID] [FILE_ID]              id of product catalog and id of file to delete'

def show_help_message():
    print(f'''
    Vtex Services is an interactive runtime terminal images integration service with Vtex
    
    Usage:
      vtex [OPTION] ARGS

    Options:
      -h, --help      help information and usage
      -i, --insert    insert new image on the catalog
      -u, --update    update variant image of catalog
      -d, --delete    delete the image of the catalog

    Args options:
    {m_args_insert}
    {m_args_update}
    {m_args_delete}
    ''')

def show_command_not_valid(command):
    print(f'\nCommand {command} is not valid.\n')

def show_params_not_valid(param):
    option_map = {
        'i': ['insert', m_args_insert],
        'u': ['update', m_args_update],
        'd': ['delete', m_args_delete]
    }
    option, message = option_map[param]

    if len(message) > 0:
      print(f'''
    Usage:
      vtex {option} ARGS

    Args options:
        {message}
        ''')

def show_env_not_valid():
    print("\n   .env is not valid.\n")
