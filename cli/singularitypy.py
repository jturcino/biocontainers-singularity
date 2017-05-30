#!/usr/bin/env python

from os import path
from json import load

token_cache = '~/.agave/current'

def get_cached_token():
    token = None
    if path.isfile(path.expanduser(token_cache)):
        with open(path.expanduser(token_cache), 'r') as f:
            token = str(load(f)['access_token'])
    return token
