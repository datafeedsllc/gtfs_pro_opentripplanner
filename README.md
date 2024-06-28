# gtfs_pro_opentripplanner

OpenTripplaner in docker works with data from https://gtfs.pro 


### Build docker
```sudo docker build -t opentripplanner .```

### Push docker
```sudo docker tag opentripplanner gtfspro/opentripplanner```

```sudo docker push gtfspro/opentripplanner:latest```

### Run docker with input commands with open port 8080
* ```sudo docker run --rm -it -p 8080:8080 opentripplanner <url_gtfs> <url_pbf>```
* or
* ```sudo docker run --rm -it -p 8080:8080 gtfspro/opentripplanner <url_gtfs> <url_pbf>```

### Run example:
* ```sudo docker run --rm -it -p 8080:8080 gtfspro/opentripplanner https://s3.gtfs.pro/files/uran/improved-gtfs-northern-ireland.zip https://download.geofabrik.de/europe/ireland-and-northern-ireland-latest.osm.pbf```

#### Route types mapping
Necessary to map the GTFS route types not supported by OTP to similar route types (including extended types)