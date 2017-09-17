#!/usr/bin/env python

import argparse
import json
import requests

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='container', required=True, help='name of biocontainers image')
    parser.add_argument('-t', dest='tag', required=True, help='tag associated with container')
    parser.add_argument('-z', dest='token', required=True, help='token for submitting job')
    parser.add_argument('-s', dest='system', choices=['jfonner-jetstream-docker2', 'jfonner-jetstream-docker3'], default='jfonner-jetstream-docker3', help='system on which to run creation job, defaults to 2')
    args = parser.parse_args()

    jobfile = 'biocontainers-resync-job.json'
    systemnum = args.system[-1:]

    # write jobfile
    with open(jobfile, 'r') as f:
        job_json = json.loads(f.read().replace('\n', ''))
    # jobnames have format 'jturcino-d2s-resync-container'
    jobname = ''.join(['jturcino-d2s-resync-', args.container])[:64]

    job_json['name'] = jobname
    job_json['appId'] = 'jturcino-docker-to-singularity-jd'+systemnum+'-0.1.0'
    job_json['executionSystem'] = args.system
    job_json['parameters']['dockerImage'] = 'quay.io/biocontainers/'+args.container
    job_json['parameters']['imageTag'] = args.tag

    with open(jobfile, 'w') as f:
        json.dump(job_json, f, sort_keys=True, indent=4, separators=(',', ': '))

    # submit job
    headers = { 'Authorization': 'Bearer '+args.token,
                'Content-Type': 'application/json'
              }
    data = open(jobfile)
    resp = requests.post('https://agave.iplantc.org/jobs/v2/?pretty=true', headers=headers, data=data)
    assert resp.status_code == 201, 'job submit error for container '+args.container+'; status code '+str(resp.status_code)

    print 'Submitted job for', args.container, args.tag, 'on system', args.system
