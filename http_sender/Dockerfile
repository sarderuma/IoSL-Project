FROM java:8-jdk-alpine
COPY ./Sender.jar ./
WORKDIR ./
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "Sender.jar"]
CMD ["java","-jar","Sender.jar"]
