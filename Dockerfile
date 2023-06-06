FROM openjdk:17-slim
#openjdk:17-ea-jdk-buster

RUN apt-get update \
&& apt-get install -y wget python3 python3-pip mc \
&& pip3 install --upgrade pip \
&& pip3 install pandas


WORKDIR /app

RUN wget https://github.com/opentripplanner/OpenTripPlanner/releases/download/v2.3.0/otp-2.3.0-shaded.jar

#todo Зачем здесь эти команды? Есть .sh скрипт run_otp.sh
CMD java -Xmx50G -jar otp-2.3.0-shaded.jar --build /data --save && \
    java -Xmx50G -jar otp-2.3.0-shaded.jar --load /data

VOLUME /data

COPY run_otp.sh /app/
COPY route_mapping.py /app/
COPY route_types_mapping.csv /app/

RUN chmod +x /app/run_otp.sh

RUN mkdir -p /data

ENTRYPOINT [ "/app/run_otp.sh" ]
