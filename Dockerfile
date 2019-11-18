FROM python:3.7-alpine
COPY / /uniparc_downloader
WORKDIR /uniparc_downloader
RUN pip install -r requirements.txt
ENTRYPOINT [ "python","uniparc_downloader.py"]