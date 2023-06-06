#!/bin/sh

if [ "$#" -ne 2 ]; then
    echo "ERROR: Missing parameters. Usage: sudo docker run --rm -it -p 8080:8080 gtfspro/opentripplanner:latest [gtfs_url] [pbf_url]"
    exit 1
fi

gtfs_url=$1
pbf_url=$2

wget $gtfs_url -P /data/
wget $pbf_url -P /data/

python3 route_mapping.py $gtfs_url

java -Xmx50G -jar /app/otp-2.3.0-shaded.jar --build /data --save && \
java -Xmx50G -jar /app/otp-2.3.0-shaded.jar --load /data


