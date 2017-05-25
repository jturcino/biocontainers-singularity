
# removed duplicate images
echo "REMOVING DUPLICATE IMAGES..."
images=`ls /scratch/03761/jturcino/biocontainers_singularity/*.img`
duplicates=`for i in $images; do echo ${i%-20??-??-??*.img}; done | cut -c 73- | uniq -d`

for i in $duplicates; do
    echo "Removing duplicates for $i"
    most_recent=`ls -t /scratch/03761/jturcino/biocontainers_singularity/quay.io_biocontainers_$i* | head -1`
    rm $most_recent
done

# remove pid, err, out files for successfully created images
echo "REMOVING PID, ERR, OUT FILES..."
pidfiles=`ls /scratch/03761/jturcino/biocontainers_singularity/*.pid`
for i in $pidfiles; do
    name=`echo ${i%.pid} | cut -c 71-`
    # Agave changes '.' in job names to '-' automatically,
    # so once we have a container name from the job name,
    # we must search for an image having '.' or '-' 
    # where the job name has a '-'.
    grep_name=`echo $name | tr - .`
    # remove pid, err, out files only if image exists
    if ! [ -z "$(ls /scratch/03761/jturcino/biocontainers_singularity/*.img | grep "_${grep_name}_.*img")" ]; then
        rm $i
        rm $(ls /scratch/03761/jturcino/biocontainers_singularity/*$name.err)
        rm $(ls /scratch/03761/jturcino/biocontainers_singularity/*$name.out)
    else
        echo "Error creating image for ${name}. Not removing its pid, err, out files."
    fi
done

# compress images
echo "COMPRESSING IMAGES..."
updated_images=`ls /scratch/03761/jturcino/biocontainers_singularity/*.img`
for i in $updated_images; do
    new_name="/scratch/03761/jturcino/biocontainers_singularity/$(echo ${i%-20??-??-??-*.img} | cut -c 73-).img"
    mv $i $new_name
    bzip2 $new_name
done

# add read-write permissions for group
# add read permissions for other
chmod g+rw *.bz2
chmod o+r *.bz2

# move compressed images to storage
#echo "MOVING IMAGES TO STORAGE..."
mv /scratch/03761/jturcino/biocontainers_singularity/*.bz2 /scratch/01114/jfonner/singularity/quay.io/biocontainers/

echo "CHECK COMPLETE"
