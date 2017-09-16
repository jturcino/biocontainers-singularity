
syncfile="resync_containers.txt"
system="jfonner-jetstream-docker3"

function refresh_token() {
	local newtoken=`echo $(auth-tokens-refresh -S) | rev | cut -d ' ' -f 1 | rev`
	echo "$newtoken"
}

# get containers to resync; store in resync_images.txt
echo "GETTING CONTAINER NAMES AND VERSIONS..."
./get-resync-containers.py -f $syncfile

# refresh and get Agave token
token=$(refresh_token)

# read in resync_images.txt
containers=`cat $syncfile | awk '{print $1}'`
tags=`cat $syncfile | awk '{print $2}'`
num_containers=`echo $containers | wc -w`

# resync containers 
echo "BEGINNING TO RESYNC CONTAINERS..."
for i in $(seq 1 $num_containers); do

    # get container, tag, and system
    container=`echo $containers | cut -d ' ' -f $i`
    tag=`echo $tags | cut -d ' ' -f $i`

    # submit to build-container.py
    ./build-container.py -c $container -t $tag -s $system -z $token

    # refresh token every 350 containers
    if [ $(( $i % 100 )) -eq 0 ]; then 
        token=$(refresh_token)
    fi

    # sleep 30s
    sleep 120
done

# remove syncfile
echo "REMOVING STORAGE FILE..."
rm $syncfile

echo "RESYNC COMPLETE"
