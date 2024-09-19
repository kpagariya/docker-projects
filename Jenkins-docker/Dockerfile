FROM jenkins/jenkins:lts

USER root
RUN apt-get update && \
    apt-get install -y maven && \
    apt-get clean
RUN apt-get install -y docker.io

USER jenkins



