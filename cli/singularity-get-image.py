#!/usr/bin/env python

import argparse
from requests import get

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Download a compressed singularity image to the specified directory.')
    parser.add_argument('-i', '--imageID', dest = 'imageID', help = 'Name of container and tag joined with an underscore, eg. container_tag')
    # name
    # tag
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', required = False, help = 'access token')
    args = parser.parse_args()

    # if token not supplied, get cached Agave token

    # build header and url
    header = {'Authorization': 'Bearer '+args.accesstoken}
    filename = args.imageID+'.img.bz2'
    url = 'https://agave.iplantc.org/singularity/v2/quay.io/biocontainers/'+filename

    # get compressed file
    resp = get(url, headers = header, stream = True)
    assert resp.status_code == 200, 'Unable to download '+args.imageID+'. HTTP status code '+str(resp.status_code)

    # write file
    with open(filename, 'wb') as f:
        for chunk in resp:
            f.write(chunk)
    print 'Successfully downloaded', args.imageID, 'as', filename, 'to the current directory.'
