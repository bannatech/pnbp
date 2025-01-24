'''
'  pnbp - pnbp is not a blogging platform
'  conf.py - encapsulate configuration handling
'  Paul Longtine <paul@banna.tech>
'''

import os
import sys
import yaml
import json

target_name = "pages.yml"
target_type = "yml"


class Configuration:
    def __init__(self):
        self.fname = target_name
        self.ftype = target_type

        self.types = {
            "yml": self.type_yml,
            "json": self.type_json
        }

    def type_yml(self):
        name = self.get_f()
        return yaml.safe_load(open(name))

    def type_json(self):
        name = self.get_f()
        return json.load(open(name))

    def get_f(self):
        if os.path.exists(self.fname):
            target_name = self.fname
            target_type = self.ftype
            return self.fname

        raise Exception("can not find suitable file {}".format(self.fname))

    def load(self):
        if self.ftype in self.types:
            return self.types[self.ftype]()
        else:
            raise Exception("unknown type {}".format(self.ftype))


def base():
    return Configuration()
