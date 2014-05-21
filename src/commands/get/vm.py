# -*-  coding:UTF-8   -*-

'''-- get vm information'''

from commands import Command

class GetVM(Command):
    id = None
    property = None
    host = None
    properties = ['id', 'property']
    
    def pre_check(self):
        print 'pre_check'
        return True, None
    
    def do_exec(self):
        print 'do_exec'
        print self.id, self.property, self.host
        return True, None
    
    def verify(self):
        print 'do_verify'
        return True, None

authenticate = lambda uname, uid, gid: uid == 0
enable = True
command_class = GetVM