# biocontainers-singularity
The scripts in this repository are used to maintain and update the library of biocontainer singularity images located on the TACC Stampede Supercomputer at `/scratch/01114/jfonner/singularity/`. 

Our biocontainer biocontainer singularity images refer to the library of life-sciences-based Docker conatiners kept by [Biocontainers](https://quay.io/organization/biocontainers). As new biocontainers are published and existing containers are updated, we use a resynchronization process to keep our Singularity collection up-to-date with the Biocontainers library.

## Resync Steps
There are three main steps in the resync process, which are explained in more depth below:
1. Get a list of new and updated containers with their most recent versions
2. Create singularity images for each of the containers in the list
3. Check that the updated images were created appropriately

### Making the list
During the resynchronization process, we want to create Singularity images of newly added containers not yet in our collection, as well as creating Singularity images of containers in our collection for which a new version has been released. To accomplish this, we first get a list of all the containers currently available in the [Biocontainers library](https://quay.io/organization/biocontainers). For each container in the list, we check if we have a Singularity image of its most recent version. If we do not, the name of the container and its most recent version is saved to `resync_containers.txt`.

### Updating Singularity images
After determining which images need to updated and added to our collection, we sumbit a job to the `jturcino-docker-to-singularity` Agave app for each container and version stored in `resync_containers.txt`. Each job outputs four files: the Singularity image, a pid file, an error file, and an output file.

### Check images
The final step in the resynchronization process ensures all new images were created correctly. First, we check for duplicate images (created from the same container and version); if found, the most recently created image is removed. Next, we check for jobs that did not create an image and delete the job files (pid, error, and output) for jobs that successfully created an image. Finally, we compress the created images using bzip2 and move them to storage at `/scratch/01114/jfonner/singularity/`.

## Resync Structure
These steps are split into four scripts:
* `get-resync-containers.py` makes and saves list of containers to be created or updated (as well as the containers' most recent versions) to `resync_containers.txt`
* `build-container.py` builds a Singularity image for a given Biocontainer Docker container when provided the container name, desired version, app execution system, and Agave access token
* `resync.sh` is a wrapper script that packages together the python scripts above
  * calls `get-resync-continaers.py` to get list of containers and versions
  * loops through list of containers
    * calls `build-container.py` to create each container
    * alternates between `jfonner-jetstream-docker2` and `jfonner-jetstream-docker3` execution systems and waits 30s between loops to avoid job overload
    * pulls a new access token every 350 loops (~175 minutes)
  * cleans up by removing `resync_containers.txt`
* `check.sh` removes duplicate containers and jobfiles that successfully produced a Singularity image, compresses Singularity images, and moves the compressed images to storage

Dividing the resynchronization process into four scripts allows this repository to be used in many ways. For example, if one simply wants to see the list of Singularity images need to be created or updated, one can run `get-resync-containers.py` independently of the resync wrapper script. Conversely, if one want to create a Singularity image of a Biocontainer with a specific version, one can run `build-container.py`. 
