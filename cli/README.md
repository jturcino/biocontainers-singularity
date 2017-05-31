# biocontainers-singularity cli
The scripts in this directory comprise a CLI with which any [Agave](https://agaveapi.co/) user can interact with the Singularity image library hosted on the `singularity-images.cyverse.org` system, hosted on the Stampede supercomputer at the [Texas Advanced Computing Center](https://www.tacc.utexas.edu/). The library references the set of life-sciences-based Docker containers maintained by [Biocontainers](https://quay.io/organization/biocontainers/). Users can look up the versions available for a given biocontainer via `singularity-list-image-versions.py` and download a compressed image from the collection via `singularity-get-image.py`.

## `singularity-list-image-versions.py`
This script takes the name of a container and returns the container versisons available in the Singularity library. Versions are listed in reverse order of creation; that is, the most recently created version is listed first. If an Agave access token is not passed in manually, the CLI will attempt to retrieve it from the Agave cache.

Below is an example where a user searches for the available versions of Bowtie. They first use the `-h`, or help flag to display all command-line options.
```
$ ./singularity-list-image-versions.py -h
usage: singularity-list-image-versions.py [-h] [-n NAME] [-z ACCESSTOKEN]

Returns all available version tags for the given biocontainer.

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  name of container
  -z ACCESSTOKEN, --accesstoken ACCESSTOKEN
                        access token
$ ./singularity-list-image-versions.py -n bowtie
1.1.2--py35_1
1.2.0--py35_0
1.2.0--py36_0
```

## `singularity-get-image.py`
This script takes in one of three input options and downloads the Singularity image associated with each option. The options are explained below using the example biocontainer Bowtie, whose available tags can be seen above. For reference, the help output of the script is below.
```
$ ./singularity-get-image.py -h
usage: singularity-get-image.py [-h] [-i IMGID] [-n NAME] [-t TAG]
                                [-z ACCESSTOKEN]

Download a compressed singularity image to the specified directory. Provide a
image ID, name and tag pair, or simply the name of the container. If only the
container name is specified, the most recent available version will be
selected.

optional arguments:
  -h, --help            show this help message and exit
  -i IMGID, --imgID IMGID
                        name of container and tag joined with an underscore,
                        eg. name_tag
  -n NAME, --name NAME  name of container
  -t TAG, --tag TAG     tag of container
  -z ACCESSTOKEN, --accesstoken ACCESSTOKEN
                        access token
```

### 1. Provide the biocontainer name and tag
If a user wishes to download the Bowtime image with tag `1.2.0--py36_0`, they can do so by passing in the name of the container and tag with the `-n` and `-t` flags, respectively.
```
$ ./singularity-get-image.py -n bowtie -t 1.2.0--py36_0
Successfully downloaded bowtie_1.2.0--py36_0 as bowtie_1.2.0--py36_0.img.bz2 to the current directory.
```

### 2. Provide the image ID
This is very similar to the previous option. An image ID is simply the biocontainer name with the tag appended by an underscore and passed in via the `-i` flag. Thus, the Bowtie biocontainer with version `1.2.0--py36_0` becomes `bowtie_1.2.0--py36_0`.
```
$ ./singularity-get-image.py -i bowtie_1.2.0--py36_0
Successfully downloaded bowtie_1.2.0--py36_0 as bowtie_1.2.0--py36_0.img.bz2 to the current directory.
```

### 3. Provide the biocontainer name only
If only the biocontainer name is provided, the most recently created corresponding image will be downloaded. For example, the most recently created Bowtie image corresponds to `1.1.2--py35_1` (first result when running `singularity-list-image-versions.py` for Bowtie); therefore, the image downloaded when only the name "bowtie" is provided will correspond to this tag.
```
$ ./singularity-get-image.py -n bowtie
Successfully downloaded bowtie_1.1.2--py35_1 as bowtie_1.1.2--py35_1.img.bz2 to the current directory.
```
