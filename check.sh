
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
pidfiles=`/scratch/03761/jturcino/biocontainers_singularity/*.pid`
for i in $pidfiles; do
    name=`echo ${i%.pid} | cut -c 71-`
    # remove pid, err, out files
    if ! [ -z "$(ls /scratch/03761/jturcino/biocontainers_singularity/*$name*.img 2>/dev/null)"]; then
        rm $i
        rm $(ls /scratch/03761/jturcino/biocontainers_singularity/*$name*.err)
        rm $(ls /scratch/03761/jturcino/biocontainers_singularity/*$name*.out)
    else
        echo "Error creating image for ${name}. Not removing its pid, err, out files."
        # TODO get info
    fi
done

# compress images
echo "COMPRESSING IMAGES..."
updated_images=`ls /scratch/03761/jturcino/biocontainers_singularity/*.img`
for i in $updated_images; do
    bzip2 $i
done

# move compressed images to storage
echo "MOVING IMAGES TO STORAGE..."
mv /scratch/03761/jturcino/biocontainers_singularity/*.bz2 /scratch/01114/jfonner/singularity/

echo "CHECK COMPLETE"
