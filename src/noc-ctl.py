#!/usr/bin/python

import sys, os
import getpass, pwd

TOOLS_HOME = os.path.abspath(os.path.dirname(__file__))

def has_directory(path):
    for file in os.listdir(path):
        if os.path.isdir(path + '/' + file):
            return True
    return False

def load_all_command_module(path):
    command_modules = dict()
    
    # load command comment
    comment = __import__(path[len(TOOLS_HOME) + 1:].replace('/', '.'), None, None, ['']).__doc__
    command_modules['__comment__'] = comment if comment else ''
    
    if has_directory(path):
        for file in os.listdir(path):
            if os.path.isdir(path + '/' + file):
                command_modules[file] = load_all_command_module(path + '/' + file)
    else:
        for file in os.listdir(path):
            if not file.startswith('__'):
                module_name = file.split('.')[0]
                module_path = path[len(TOOLS_HOME) + 1:] + '/' + module_name
                try:
                    mod = __import__(module_path.replace('/', '.'), None, None, [''])
                except ImportError:
                    continue
                
                if getattr(mod, 'enable', True):
                    command_modules[module_name] = mod
                    
    return command_modules

def show_commands_in_context(all_command_module):
    print 'Aavailable commands:\n'
    
    for command in all_command_module:
        if command != '__comment__':
            if isinstance(all_command_module[command], dict):
                print '%-30s %s' % (command, all_command_module[command]['__comment__'])
            else:
                print '%-30s %s' % (command, all_command_module[command].__doc__)
            
    print ''

def find_command_module(all_command_module):
    arg_index = 1
    for command in sys.argv[1:]:
        arg_index = arg_index + 1
        if command in all_command_module:
            if isinstance(all_command_module.get(command), dict):
                all_command_module = all_command_module.get(command)
            else:
                return (all_command_module.get(command), sys.argv[arg_index:])
        else:
            print 'ERROR: command not found'
            break
    
    show_commands_in_context(all_command_module)
    return (None, None)
    
def parse_and_set_args(command_instance, argv):
    args = list()
    kwargs = dict()
    
    for arg in argv:
        if arg.find('=') > 0:
            arg_split = arg.split('=')
            kwargs[arg_split[0]] = arg_split[1] if len(arg_split) > 1 else ''
        else:
            args.append(arg)
            
    if kwargs:
        for key in kwargs:
            if hasattr(command_instance, key):
                setattr(command_instance, key, kwargs[key])
    else:
        properties = type(command_instance).__dict__.get('properties')
        if properties:
            for index in range(len(args) if len(args) < len(properties) else len(properties)):
                setattr(command_instance, properties[index], args[index])
                
def get_current_user():
    user = getpass.getuser()
    pwdinfo = pwd.getpwnam(user)
    return user, pwdinfo.pw_uid, pwdinfo.pw_gid
            

if __name__ == '__main__':
    
    # load all commands
    all_command_module = load_all_command_module(TOOLS_HOME + '/commands')
    
    # match command to python module
    command_module, argv = find_command_module(all_command_module)
    
    if command_module:
        # check user
        user_info = get_current_user()
        authenticate = getattr(command_module,'authenticate', None)
        if not authenticate or not authenticate(*user_info):
            print "ERROR: Current user has no privilege to execute the command"
            exit()
            
        command_instance = getattr(command_module, 'command_class')()
        if argv:
            parse_and_set_args(command_instance, argv)
            
        result, message = command_instance.pre_check()
        if not result:
            exit()
            
        result, message = command_instance.do_exec()
        if not result:
            exit()
            
        result, message = command_instance.verify()
        if not result:
            exit()