#!/usr/bin/env bash

# presets
scratch="/scratch/03761/jturcino/biocontainers_singularity/"
storage="/work/projects/singularity/TACC/biocontainers/"
img_info="resync_containers.txt"
jobname_prefix="jturcino-d2s-resync-"

# remove duplicate images
echo "REMOVING DUPLICATE IMAGES..."
images=`ls $scratch*.img`
duplicates=`for i in $images; do echo ${i%-20??-??-??*.img}; done | cut -c 73- | uniq -d`
for i in $duplicates; do
    echo "Removing duplicates for $i"
    most_recent=`ls -t ${scratch}quay.io_biocontainers_$i* | head -1`
    rm $most_recent
done

# rename images
echo "RENAMING IMAGES..."
updated_images=`ls ${scratch}*.img`
for i in $updated_images; do
    new_name="${scratch}$(echo ${i%-20??-??-??-*.img} | cut -c 73-).img"
    mv $i $new_name
done

# add read-write permissions for group and read permissions for other
echo "UPDATING PERMISSIONS..."
chmod g+rw $scratch*.img
chmod o+r $scratch*.img


# check for errors and remove pid, err, and out files
echo "CHECKING FOR ERRORS..."
containers=`cat $img_info | awk '{print $1}'`
tags=`cat $img_info | awk '{print $2}'`
num_containers=`cat $img_info | wc -l`

for i in $(seq 1 $num_containers); do
    container=`echo $containers | cut -d ' ' -f $i`
    tag=`echo $tags | cut -d ' ' -f $i`
    image="${scratch}${container}_${tag}.img"
    jobname="${scratch}${jobname_prefix}$(echo $container | tr '.' '-')"
    # rm jobfiles only if both pid and img files exist
    if [ -e "$image" ] && [ -e "${jobname}.pid" ]; then
        rm ${jobname}.pid
        rm ${jobname}.err
        rm ${jobname}.out
    # do not remove jobfiles if no img file created; error in job
    elif ! [ -e "$image" ] && [ -e "${jobname}.pid" ]; then
        echo "Image not created for ${container}_${tag}. Not removing pid, err, or out file."
    # inform user if not jobfiles created for a container; error in submission
    else
        echo "Error submitting job for ${container}_${tag}. No jobfiles produced."
    fi
done

# move compressed images to storage
echo "MOVING IMAGES TO STORAGE..."
mv $scratch*.img $storage

# remove image info file
rm $img_info

echo "CHECK COMPLETE"
