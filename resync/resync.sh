#!/usr/bin/env bash

function refresh_token() {
    local newtoken=`echo $(auth-tokens-refresh -S) | rev | cut -d ' ' -f 1 | rev`
    echo "$newtoken"
}

syncfile="resync_containers.txt"
system="jfonner-jetstream-docker3"
tag="latest"
HELP="
This script orchestrates the generation of multiple singularity images using the 
Agave docker-to-singularity app. When run in its default state (no options provided), 
it updates the repository of quay.io biocontainers images on Stampede2. If the user 
has their own list of images to generate, they can be provided in a formatted text 
file: one line per container, with container and tag separated by a space.

Usage: ./resync.sh [OPTIONS]

Options:
  -h, --help		show this help message and exit
  -f, --syncfile 	name of the syncfile from which to read containers and tags
  -z, --token		token with which to submit jobs to the system
  -s, --system		execution system with docker-to-singularity app
"

# argparse
while [[ $# -gt 1 ]]; do
    key="$1"
    case $key in
        -f|--syncfile) shift;
            syncfile="$1"
            shift ;;
        -z|--token) shift;
            token="$1"
            shift ;;
        -s|--system) shift;
            system="$1"
            shift ;;
        *)
            echo "$HELP"
            exit 0
    esac
done

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    echo "$HELP"
    exit 0
fi

# if syncfile not present, get containers to resync
if ! [ -e "$syncfile" ]; then
    echo "GETTING CONTAINER NAMES AND VERSIONS..."
    ./get-resync-containers.py -f $syncfile
fi

# read in resync_containers.txt
containers=`cat $syncfile | awk '{print $1}'`
tags=`cat $syncfile | awk '{print $2}'`
num_containers=`echo $containers | wc -w`

# refresh Agave token if not provided
if [ -z "$token" ]; then
    token=$(refresh_token)
fi

# resync containers 
echo "BEGINNING TO RESYNC CONTAINERS..."
for i in $(seq 1 $num_containers); do

    # get container, tag, and system
    container=`echo $containers | cut -d ' ' -f $i`
    tag=`echo $tags | cut -d ' ' -f $i`

    # submit to build-container.py
    ./build-container.py -c $container -t $tag -s $system -z $token

    # refresh token every 100 containers
    if [ $(( $i % 100 )) -eq 0 ]; then 
        token=$(refresh_token)
    fi
    sleep 120
done

echo "RESYNC COMPLETE"
