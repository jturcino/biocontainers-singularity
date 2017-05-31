#!/usr/bin/env python

import argparse
import singularitypy
from requests import get

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Returns all available version tags for the given biocontainer.')
    parser.add_argument('-n', '--name', dest = 'name', help = 'name of container')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', required = False, help = 'access token')
    args = parser.parse_args()

    # if token not supplied, get cached Agave token
    if args.accesstoken is None:
        args.accesstoken = singularitypy.get_cached_token()
        assert args.accesstoken is not None, 'Could not read cached token.'

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
    image_list = [ x for x in total_image_list if i[:len(name_suffix)] == name_suffix ]

    if len(image_list) == 0:
        print 'There are currently no images available for the biocontainer', args.name
    else:
        for i in image_list:
            print i[len(name_suffix):]
