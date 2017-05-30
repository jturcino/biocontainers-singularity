#!/usr/bin/env python

import argparse
import singularitypy
from sys import exit as ex
from requests import get

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Download a compressed singularity image to the specified directory. Provide a image ID, name and tag pair, or simply the name of the container. If only the container name is specified, the most recent available version will be selected.')
    parser.add_argument('-i', '--imgID', dest = 'imgID', help = 'name of container and tag joined with an underscore, eg. name_tag')
    parser.add_argument('-n', '--name', dest = 'name', help = 'name of container')
    parser.add_argument('-t', '--tag', dest = 'tag', help = 'tag of container')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', required = False, help = 'access token')
    args = parser.parse_args()

    # if token not supplied, get cached Agave token
    if args.accesstoken is None:
        args.accesstoken = singularitypy.get_cached_token()
        assert args.accesstoken is not None, 'Could not read cached token.'

    # build image ID (name_tag) if args.imgID is not used
    if args.imgID is None:
        # if name and tag pair is given, join with an underscore
        if args.name is not None and args.tag is not None:
            args.imgID = args.name+'_'+args.tag

        # if only name is given, find most recent tag
        elif args.name is not None:
            ex('Code not implemented for only name given')

        # if nothing given, exit with error
        else:
            ex('One of three options must be provided: an image ID, a container name, or a container name and tag pair.')

    # build header and url
    header = {'Authorization': 'Bearer '+args.accesstoken}
    filename = args.imgID+'.img.bz2'
    url = 'https://agave.iplantc.org/singularity/v2/quay.io/biocontainers/'+filename

    # get compressed file
    resp = get(url, headers = header, stream = True)
    assert resp.status_code == 200, 'Unable to download '+args.imgID+'. HTTP status code '+str(resp.status_code)

    # write file
    with open(filename, 'wb') as f:
        for chunk in resp:
            f.write(chunk)
    print 'Successfully downloaded', args.imgID, 'as', filename, 'to the current directory.'
