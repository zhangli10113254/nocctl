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
        print 'command info'
    
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
    def defautl_value(self):
        return self._default_value
    
    @property
    def help_info(self):
        return self._help_info
    
    def _set_value(self, value):
        self._value = value
        
    def _get_value(self):
        if hasattr(self, '_value'):
            return self._value
        return self.defautl_value if self.defautl_value else None
    
    value = property(_get_value, _set_value)