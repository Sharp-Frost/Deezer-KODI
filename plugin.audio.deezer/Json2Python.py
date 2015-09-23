'''
Created on 18 juin 2012

@author: Sharp-Frost
'''
import urllib2
import json
import DeezerDomain

__domainModuleName__='DeezerDomain'


class Json2Python(json.JSONDecoder):
    
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        if 'type' in d:
            class_name = d.pop('type').lower().capitalize()
            module_name = __domainModuleName__
            module = __import__(module_name)
            class_ = getattr(module, class_name)
            args = dict( (key.encode('ascii'), value) for key, value in d.items())
            inst = class_()
            for key,value in args.items():
                setattr(inst, key, value)
        elif 'artist' in d:
            class_ = getattr(__domainModuleName__, 'Artist')
            args = dict( (key.encode('ascii'), value) for key, value in d.items())
            inst = class_()
            for key,value in args.items():
                setattr(inst, key, value)
        elif 'album' in d:
            class_ = getattr(__domainModuleName__, 'Album')
            args = dict( (key.encode('ascii'), value) for key, value in d.items())
            inst = class_()
            for key,value in args.items():
                setattr(inst, key, value)
        else:
            inst = d
        return inst
