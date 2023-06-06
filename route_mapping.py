import pandas as pd
import zipfile
import os
import sys
import tempfile
import shutil

# Data directory
dir_data = '/data'
# Get URL from input arguments
gtfs_url = str(sys.argv[1])
# Extract the archive name from the URL to work with
archive = gtfs_url.split("/")[-1]

# Load route_types_mapping.csv into a pandas dataframe
mapping_df = pd.read_csv('route_types_mapping.csv')

# Define function to remove file from zip
def remove_from_zip(zipfname, *filenames):
    tempdir = tempfile.mkdtemp()
    try:
        tempname = os.path.join(tempdir, 'new.zip')
        with zipfile.ZipFile(zipfname, 'r') as zipread:
            with zipfile.ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in filenames:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
        shutil.move(tempname, zipfname)
    finally:
        shutil.rmtree(tempdir)

# Change the current directory to the data directory
os.chdir(dir_data)

# Extract the 'routes.txt' file
with zipfile.ZipFile(archive, 'r') as zip_file:
    zip_file.extract('routes.txt')

# Load routes.txt into a pandas dataframe
routes_df = pd.read_csv('routes.txt')

# Replace unsupported route types with supported ones using mapping
routes_df['route_type'].replace(dict(zip(mapping_df['route_type_in'], mapping_df['route_type_out'])), inplace=True)

# Save the result to 'routes.txt'
routes_df.to_csv('routes.txt', index=False)

# Remove the 'routes.txt' file from the original archive
remove_from_zip(archive, 'routes.txt')

# Add the 'routes.txt' file to the original archive
with zipfile.ZipFile(archive, 'a') as z:
    z.write('routes.txt')

# Delete the temporary 'routes.txt'
os.remove('routes.txt')
