import sys

class Command(object):
    
    def __init__(self):
        self._arguments = list()
        self._arguments_dict = dict()
        self._regist_arguments()
    
    def _regist_argumemt(self, name, type, default_value = None, help_info = None):
        arg = Argument(name, type, default_value, help_info)
        self._arguments.append(arg)
        self._arguments_dict[name] = arg
    
    def _get_argument(self, name):
        return self._arguments_dict.get(name, None)
    
    def _get_arguments(self):
        return self._arguments
    
    def _regist_arguments(self):
        raise NotImplementedError()
    
    def _show_command_info(self):
        _command_module = type(self).__dict__['__module__']
        _command = 'noc-ctl'
        for package in _command_module.split('.')[1:]:
            _command = _command + ' ' + package
    
        for argument in self._get_arguments():
            if not argument.default_value:
                _command = '%s [%s=]<%s>' % (_command, argument.name, argument.type)
            else:
                _command = '%s [[%s=]<%s>]' % (_command, argument.name, argument.type)
                
        print 'Usage: %s\n' % _command
        
        _arg_format = '\t %-20s %-15s %-20s %s'
        print 'Arguments:'
        print _arg_format % ('<name>', '<type>', '<default value>', '<detail>')
        for argument in self._get_arguments():
            print _arg_format % (argument.name, argument.type, argument.default_value, argument.help_info)
        print ''
    
    def pre_check(self):
        raise NotImplementedError()
    
    def do_exec(self):
        raise NotImplementedError()
    
    def verify(self):
        raise NotImplementedError()
    
class Argument(object):    
    def __init__(self, name, type, default_value = None, help_info = None):
        self._name = name
        self._type = type
        self._default_value = default_value
        self._help_info = help_info
        
    @property
    def name(self):
        return self._name
    
    @property
    def type(self):
        return self._type
    
    @property
    def default_value(self):
        return self._default_value
    
    @property
    def help_info(self):
        return self._help_info
    
    def _set_value(self, value):
        self._value = value
        
    def _get_value(self):
        if hasattr(self, '_value'):
            return self._value
        return self.default_value if self.default_value else None
    
    value = property(_get_value, _set_value)