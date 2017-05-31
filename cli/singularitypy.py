#!/usr/bin/env python

from os import path
from json import load
from requests import get
from datetime import datetime

token_cache = '~/.agave/current'

def get_cached_token():
    token = None
    if path.isfile(path.expanduser(token_cache)):
        with open(path.expanduser(token_cache), 'r') as f:
            token = str(load(f)['access_token'])
    return token

def get_newest_img_tag(container, token):
    
    # get all images
    header = {'Authorization': 'Bearer '+token}
    url = 'https://agave.iplantc.org/singularity/v2/quay.io/biocontainers/'
    resp = get(url, headers = header)
    assert resp.status_code == 200, 'Unable to list singularity images. HTTP status code '+str(resp.status_code)
    resp = resp.json()
    
    # get IDs and times of images corresponding to given container
    img_time_list = [ {'name': str(x.get('name')), 'time':str(x.get('lastModified')[:-10])} for x in resp['result'] if x['name'][:len(container)] == container ] 
    
    for i in img_time_list:
        datetime_obj = datetime.strptime(i.get('time'), '%Y-%m-%dT%H:%M:%S')
        i['time'] = datetime_obj
    img_time_list.sort()

    newest_img = img_time_list[0]
    return newest_img[len(container)+1 : -8]
