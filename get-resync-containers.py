#!/usr/bin/env python

import argparse
import os
import requests
import json
from datetime import datetime
from operator import itemgetter

def get_most_recent_tag(repo):
    url = 'https://quay.io/api/v1/repository/biocontainers/' + repo
    resp = requests.get(url)
    assert resp.status_code == 200, 'Status code for '+repo+' = '+str(resp.status_code)+' != 200'

    tags = resp.json()['tags']
    try:
        assert len(tags.keys()) > 0#, 'No tags for '+repo
    except:
        return

    tag_datetime_list = []
    for i in tags:
        datetime_str = tags[i]['last_modified'][5:-6]
        datetime_obj = datetime.strptime(datetime_str, '%d %b %Y %H:%M:%S')
        tag_datetime_list.append( (i, datetime_obj) )
    tag_datetime_list.sort(key=itemgetter(1), reverse=True)

    return tag_datetime_list[0][0]

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--savefile', dest='savefile', help='name of savefile for images to be synced')
    args = parser.parse_args()
    
    biocontainers_url = 'https://quay.io/api/v1/repository?public=true&namespace=biocontainers'
    resp = requests.get(biocontainers_url)
    assert resp.status_code == 200
    resp = resp.json()
    available_repos = [ str(x['name']) for x in resp['repositories'] ]

    storage_dir = '/scratch/01114/jfonner/singularity/'
    current_images = [ x[22:-32] for x in os.listdir(storage_dir) if x[-3:] == 'bz2' ]

    # COMBINE NEW AND REDO REPOS
    #new_repos = [ repo for repo in available_repos if not any(repo in image for image in current_images) ]
    resync_containers = [] # entries formatted as (repo, version)
    for repo in available_repos:
        # first 'any' checks for instance of repo in current images 
        # (repo'_' assures no confusion in situations such as *bowtie_version* and *bowtie2_version*)
        # second 'any' checks the current image has the most recent version if the first clause passes
        most_recent_tag = get_most_recent_tag(repo)
        if most_recent_tag is None:
            print 'Empty', repo
            continue
        if not ( any(repo+'_' in image for image in current_images) or any(repo+'_'+most_recent_tag == image for image in current_images) ):
            print 'Resync', repo
            resync_containers.append( (repo, most_recent_tag) )
        else:
            print 'Ignore', repo

    # write to file 
    # this way we don't have to worry about more than 480 jobs
    with open(args.savefile, 'w') as f:
    	for i in resync_containers:
    	    s = i[0] + ' ' + i[1] + '\n'
    	    f.write(s)
