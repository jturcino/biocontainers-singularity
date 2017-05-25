# biocontainers-singularity resync
The scripts in this repository are used to maintain and update the library of biocontainer singularity images located on the `singularity-images.cyverse.org` system, hosted by the Stampede Supercomputer at the [Texas Advanced Computing Center](https://www.tacc.utexas.edu/). 

Our biocontainer Singularity images reference the library of life-sciences-based Docker conatiners kept by [Biocontainers](https://quay.io/organization/biocontainers). As new containers are published and existing containers are updated, we use a resynchronization process to keep our Singularity collection up-to-date with the Biocontainers library.

## Resync Steps
There are three steps in the resync process:
1. Obtain a list of new and updated containers with their most recent versions
2. Create Singularity images for each of the container-version pairs in the list
3. Check the Singularity images were created appropriately

### Making the list
During the resynchronization process, we create Singularity images of newly added containers not yet in our collection, as well as creating Singularity images of containers in our collection for which a new version has been released. To accomplish this, we first obtain a list of all the containers currently available in the [Biocontainers library](https://quay.io/organization/biocontainers). For each container in the list, we check if a Singularity image of its most recent version exists in our library. If not, the name of the container and its most recent version is saved to `resync_containers.txt`.

### Updating Singularity images
After determining which images need to updated or added to our collection, we sumbit a job to the `jturcino-docker-to-singularity` Agave app for each container-version pair stored in `resync_containers.txt`. Each job outputs four files: the Singularity image, a pid file, an error file, and an output file.

### Check images
The final step in the resynchronization process ensures all new images were created correctly. First, we check for duplicate images (created from the same container-version pair); if found, the most recently created image is removed. Next, we delete the job files (pid, error, and output) for jobs that successfully created an image. Finally, we compress the created images using `bzip2` and move them to storage on the `singularity-images.cyverse.org` system.

## Resync Structure
These steps are split into four scripts:
* `get-resync-contianers.py`
* `build-container.py`
* `resync.sh`
* `check.sh`

### `get-resync-containers.py` 
This python script performs the "Making a list" step detailed above. It retrieves the a list of all Docker containers currently in the [Biocontainers library](https://quay.io/organization/biocontainers) and saves the container-versions pairs of new and updated containers to a user-provided save file.

### `build-container.py` 
This python script submits a job to the `jturcino-docker-to-singularity` Agave app, thus building a Singularity image for a given Biocontainer Docker container. It does not rely upon `get-resync-containers.py` in any way; thus it can be used to produce a Singularity image of any Biocontainers Docker container with any version. It requires a user-provided container name, version, app execution system, and valid Agave access token.

### `resync.sh` 
This shell script acts as a resychronization wrapper script that packages together the python scripts above to execute initial two steps of the resynchronization process. It calls `get-resync-continaers.py` to obtain a list of container-version pairs stored in `resync_containers.txt`. It then loops through the container-version pairs, calling `build-container.py` to create each Singularity image. In order to avoid overloading the execution system, it alternates between the `jfonner-jetstream-docker2` and `jfonner-jetstream-docker3` execution systems and waits 30s between loops. Additionally, `resync.sh` pulls a new access token every 350 loops. After submitting jobs for all container-verison pairs, the wrapper script removes `resync_containers.txt`.

### `check.sh` 
This shell script is to be executed by the user some time after `resync.sh` finishes and all `jturcino-docker-to-singularity` jobs are completed. It fulfills the third step of the resynchronization process. As its name implies, it serves to check and clean up the output of `resync.sh` by removing duplicate containers and jobfiles that successfully produced a Singularity image. It also compresses the produced Singularity images and moves them to storage on the `singularity-images.cyverse.org` system.

Dividing the resynchronization process into four scripts allows this repository to be used in many ways. For example, if one simply wants to see the list of Singularity images need to be created or updated, one can run `get-resync-containers.py` independently of the resync wrapper script. Conversely, if one want to create a Singularity image of a Biocontainer with a specific version, one can run `build-container.py`. 
