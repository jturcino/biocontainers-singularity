#!/usr/bin/env python

import argparse
from requests import get

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Download a compressed singularity image to the specified directory.')
    parser.add_argument('-n', '--name', dest = 'name', help = 'name of container')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', required = False, help = 'access token'
    args = parser.parse_args()

    # if token not supplied, get cached Agave token

    # build header and url
    header = {'Authorization': 'Bearer '+args.accesstoken}
    url = 'https://agave.iplantc.org/singularity/v2/quay.io/biocontainers/'

    # get list of all images
    resp = get(url, headers = header)
    assert resp.status_code == 200, 'Unable to list singularity images. HTTP status code '+str(resp.status_code)
    resp = resp.json()
    total_image_list = [ str(i['name']) for i in resp['result'] ]

    # print images corresponding to given container name
    name_suffix = name+'_'
    for i in total_image_list:
        if i[:len(name_suffix)] == name_suffix:
            print i
