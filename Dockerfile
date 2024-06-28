FROM openjdk:24-slim
#openjdk:17-ea-jdk-buster

# Install necessary packages
RUN apt-get update \
    && apt-get install -y wget python3 python3-pip mc python3-pandas \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Download the OpenTripPlanner jar file
RUN wget https://github.com/opentripplanner/OpenTripPlanner/releases/download/v2.5.0/otp-2.5.0-shaded.jar

# Define the CMD to build and load OTP data
CMD java -Xmx50G -jar otp-2.5.0-shaded.jar --build /data --save && \
    java -Xmx50G -jar otp-2.5.0-shaded.jar --load /data

# Define the data volume
VOLUME /data

# Copy the application scripts and data
COPY run_otp.sh /app/
COPY route_mapping.py /app/
COPY route_types_mapping.csv /app/

# Make the script executable
RUN chmod +x /app/run_otp.sh

# Create a data directory
RUN mkdir -p /data

# Set the entry point for the container
ENTRYPOINT [ "/app/run_otp.sh" ]
