The purpose of this project is to be able to import albums from Google photos into Immich if the image files already exists in immich.
The python script uses the filename of the image to locate the exact same filename in Immich.

The python script will create a album if it does not alreadt exist.
If an image cannot be located a warning will be printed but the script will continue.
The name of the albums will be based on the name of the folders found in the directory supplied with the argument "--root-folder"

## Example

Download your two albums from Google photos and extract the files in two folders, foo and bar.
The foo album will contain foo.jpg.
The bar album will contain bar.jpg

- /albums/foo/
  - foo.jpg
- /albums/bar
  - bar.jpg

Using the following command the script will be invoked to create the albums in Immich:
python3 ./immich_import.py --root-folder="/albums" --immich-url="http://SERVER_IP:PORT/api" --api-key="API_KEY"

The argument "--dry-run" can be supplied to simulate the execution.
