FROM ubuntu:22.04

# install python3 and pip3
RUN apt update
RUN apt install -y python3 python3-pip

# make frontend directory
RUN mkdir /metadata

# copy the requirements file to the container
COPY requirements.txt /metadata/requirements.txt

# install the requirements
RUN pip3 install -r /metadata/requirements.txt

# copy the rest of the application to the container
COPY . /metadata

# set the working directory
WORKDIR /metadata

# expose the port
EXPOSE 9000

# run the application
CMD ["python3", "main.py"]
