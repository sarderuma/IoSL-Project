# TUB-IoSL-Sender

**Author: Liming Liu	 liming.liu@campus.tu-berlin.se**

**Overview:** 

Goal: This Java project is intended to serve as the traffic sender for testing the performance of 2 different communication paradigms. 

Function: To initiate a server that generates packets to a destination, and the sending process is able to be started/stopped from user dash board. 

	
**Package structure:** 

1. sender/main provides the entry point of the program 

2. sender/controller provides 2 classes that executes service logic

3. sender/util provides several utility classes for network communication and Jaeger tracer configuration

4. sender/test provides a dummy client and a dummy receiver inteded for testing

5. extra files:

    --pom.xml declares the dependencies

    --Dockerfile used to dockerize the project into a docker container

    --Sender.jar a backup runnable jar file for dockerization


**Deploy:**

This project is intended to be running in a docker container environment, thus the first step is to pack the project into a .jar file, then dockerize it and push to docker hub if needed

Step1:

Unless you want to change the code, you can skip this step and use the backup jar file provided in the package. However if you need to change the code please follow the instructions below to repack the project.

Recommended way to pack the project is by using IDEs like Intellij or Eclipse, first import the project and then go to **File->Export->Runnable Jar File->select sender.main.SenderLauncher as main clas->Finish**


Alternative, but less reliable way to pack the project is by using command line tool, for instance in Linux:

```Linux
$jar cvfm (work location)/sender.jar MANIFEST.MF -C . .
```

Step2:

Command for dockerization:

```Linux
$cp Dockerfile (work location)/Dockerfile
$cd (work location)
$sudo docker build -t sender-image .
$sudo docker tag sender-image iosl/sender:(some tag)
$sudo docker push iosl/sender:(some tag)
```
	


	
