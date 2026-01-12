# Simple OPDS

Simple OPDS is a lightweight python implementation of the [OPDS 1.2](https://specs.opds.io/opds-1.2) spec.

## Features

### Custom Directory

 - Will automatically scan and display the exact folder structure in the OPDS feed.
 - Does not support having files and folders in the same directory (As specified in the OPDS 1.2 documentation).

### Upcoming Features

 - More customisation using environment variables.
 - Parsing file metadata for thumbnails and descriptions.
 - Support for more filetypes.
 - Searching, and webcrawling support.
 - Pages for large libraries.
 - Authentication (login or token-based).

## Options

Options can be set using environment variables. They can either be loaded directly from the host system, from a
`.env` file, or as environment options passed through to a docker container.

- LIBRARY_PATH: Designates the folder that contains all content to be made available by the OPDS server. (Default: './content')
- PORT: Which port the server should listen on. (Default: 5000)