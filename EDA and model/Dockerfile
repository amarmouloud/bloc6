FROM python:3.7-slim-buster
WORKDIR /Users/marion/Documents/Jedha/Jedha-Certification/Bloc 6
COPY . .
RUN apt-get update && apt-get -y update
RUN apt-get install -y build-essential python3-pip python3-dev
RUN pip3 -q install pip --upgrade
#RUN pip3 install mljar-supervised jupyterlab
RUN pip3 install -r requirements.txt
EXPOSE 8888
CMD ["jupyter", "lab", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.password=''","--NotebookApp.token=''"]