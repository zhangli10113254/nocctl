# -*-  coding:UTF-8   -*-

'''
Created on 2014年5月21日

@author: zhangli
'''
import os

class FileConfig(object): 
    def __init__(self, file_path):
        self.params = dict()
        self.params_commentary = dict()
        self.file_path = os.path.abspath(file_path)
        if self.exist():
            self._read()
    
    def _read(self):
        raise NotImplementedError()
    
    def exist(self):
        return os.path.exists(self.file_path) and os.path.isfile(self.file_path)
    
    def save(self):
        if self.exist():
            # cp original file to temp file
            temp_file = self.file_path + '_temp'
            if os.system('cp -a %s %s' % (self.file_path, temp_file)) != 0:
                raise IOError('Can not create temp file!')
            
            # save all config to temp file
            self._do_save(self.file_path, temp_file)
            
            # cover original file with temp file
            if os.system('cp -a %s %s' % (temp_file, self.file_path)) != 0:
                raise IOError('cover original file with temp file fail')
            
            # remove temp file
            os.remove(temp_file)
        else:
            # if config file is a new file, create and write directly
            self._do_save(None, self.file_path)
    
    def _do_save(self, original_file = None):
        raise NotImplementedError()
    
    def get(self, key):
        return self.params.get(key, None)
    
    def set(self, key, value, commentary = None):
        self.params[key] = value
        if commentary:
            self.params_commentary[key] = commentary
        
    def delele(self, key):
        if key in self.params:
            del self.params[key]
            

class PropertyFileConfig(FileConfig):
    def __init__(self, file_path):
        FileConfig.__init__(self, file_path)
    
    def _read(self):
        with open(self.file_path, 'r') as f:
            for line in f:
                line = line.strip()
                split_index = line.find('=')
                if not line.startswith('#') and split_index != -1:
                    key = line[:split_index].strip()
                    value = line[split_index + 1:].strip()
                    self.params[key] = value
                    
    def _do_save(self, original_file, temp_file):
        with open(temp_file, 'w') as out_f:
            if original_file:
                with open(original_file, 'r') as in_f:
                    for line in in_f:
                        line = line.strip()
                        split_index = line.find('=')
                        if not line.startswith('#') and split_index != -1:
                            key = line[:split_index].strip()
                            if key in self.params:
                                value = self.params[key]
                            else:
                                continue
                            
                            out_f.write("%s=%s\n" % (key, value))
                            del self.params[key]
                        else:
                            out_f.write(line + '\n')
                    
            for key, value in self.params.iteritems():
                if key in self.params_commentary:
                    out_f.write('#' + self.params_commentary[key] + '\n')
                out_f.write("%s=%s\n" % (key, value))