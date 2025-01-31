FROM ubuntu:22.04

# install python3 and pip3
RUN apt update
RUN apt install -y python3 python3-pip

# make frontend directory
RUN mkdir /frontend

# copy the requirements file to the container
COPY requirements.txt /frontend/requirements.txt

# install the requirements
RUN pip3 install -r /frontend/requirements.txt

# copy the rest of the application to the container
COPY . /frontend

# set the working directory
WORKDIR /frontend

# expose the port
EXPOSE 8000

# run the application
CMD ["python3", "main.py"]
