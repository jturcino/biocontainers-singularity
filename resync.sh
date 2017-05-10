
syncfile="resync_containers.txt"

echo 'GETTING CONTAINER NAMES AND VERSIONS...'
# get containers to resync; store in resync_images.txt
./get-resync-containers.py -f $syncfile
# refresh and get Agave token
token=`echo $(auth-tokens-refresh -S) | rev | cut -d ' ' -f 1 | rev`

# read in resync_images.txt
containers=`cat $syncfile | awk '{print $1}'`
tags=`cat $syncfile | awk '{print $2}'`
num_containers=`echo $containers | wc -w`

echo 'BEGINNING TO RESYNC CONTAINERS...'
# resync containers 
for i in $(seq 1 $num_containers); do
	# get container, tag, and system
	container=`echo $containers | cut -d ' ' -f $i`
	tag=`echo $tags | cut -d ' ' -f $i`
	system="jfonner-jetstream-docker$(( $i%2+2 ))"
	# submit to sync-container.py
	./sync-container.py -c $container -t $tag -s $system -z $token

	# sleep 30s
	sleep 30
done

echo 'REMOVING STORAGE FILE...'
# remove syncfile
rm $syncfile

echo 'RESYNC COMPLETE'