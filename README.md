# Simple OPDS

Simple OPDS is a lightweight implementation of the [OPDS 1.2](https://specs.opds.io/opds-1.2) spec.

## Features

### Custom Directory

 - Will automatically scan and display the exact folder structure in the OPDS feed.
 - Does not support having files and folders in the same directory (As specified in the OPDS 1.2 documentation).

### Upcoming Features

 - More customisation using environment variables.
 - Parsing file metadata for thumbnails and descriptions.
 - Support for more filetypes


## Options

Options can be set using environment variables. They can either be loaded directly from the host system, from a
`.env` file, or as environment options passed through to a docker container.

- LIBRARY_PATH: Designates the folder that contains all content to be made available by the OPDS server. (Default: './content')