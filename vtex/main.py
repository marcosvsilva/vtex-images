import sys
from dotenv import load_dotenv
from api import run
from messages import *

load_dotenv()

num_args = len(sys.argv)

def split_arguments(args):
    op, new_args = '0', []
    if not args:
        show_help_message()

        
    if len(args) > 0:    
        option = args[0]
        
        if option in ['-h', '--help']:
            show_help_message()
        else:
            if option in ['-i', '--insert', '-u', '--update', '-d', '--delete']:
                action = [c for c in option if c != '-'][0]

                if len(args) not in [3, 4]:
                    show_params_not_valid(action)
                else:
                    return action, args[1:]
            else:
                show_command_not_valid(option)
        
    return op, new_args

def main(args):
    op, args = split_arguments(args)
    if op in ['i', 'u', 'd']:
        run(op, args)

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
