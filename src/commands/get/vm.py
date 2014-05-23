# -*-  coding:UTF-8   -*-

'''-- get vm information'''

from commands import Command

class GetVM(Command):
    def __init__(self):
        Command.__init__(self)
    
    def pre_check(self):
        if self._get_argument('id').value is None:
            return -1
        return 0
    
    def do_exec(self):
        print 'do_exec'
        print self._get_argument('id').value
        print self._get_argument('name').value
        return True
    
    def verify(self):
        print 'do_verify'
        return True
    
    def _regist_arguments(self):
        self._regist_argumemt('id', int, default_value = None, help_info = 'vm id')
        self._regist_argumemt('name', str, default_value = None, help_info = 'vm name')

authenticate = lambda uname, uid, gid: True
enable = True
command_class = GetVM