# biocontainers-singularity
This repository container two sets of scripts, both of which pertain to the library of biocontainer Singularity images located on the `singularity-images.cyverse.org` system, hosted on the Stampede Supercomputer at the [Texas Advanced Computer Center](https://www.tacc.utexas.edu/). Our biocontainer Singularity images reference the library of life-sciences-based Docker containers maintained by [Biocontainers](https://quay.io/organization/biocontainers/).

# CLI
The CLI allows any user with an Agave access token to interact with the biocontainer image library. Users can browse available image versions for a given biocontainer and download a compressed image for personal use. A more in-depth description of CLI functionality is given in the CLI readme, located in the `cli` directory.

# Resync
As new biocontainers are made available and existing biocontainers are updated, we use a resynchronization process to keep our Singularity image library up-to-date with the Biocontainers library. The scripts used to perform this resynchronization, located in the `resync` directory, are not executable by the general public due to the use of several private Agave applications and systems. However, the code and an explanatory readme are available to those interested in how we maintain our biocontainer image library.
