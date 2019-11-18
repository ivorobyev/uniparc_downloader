FROM python:3.7-alpine
COPY / /uniparc_downloader
WORKDIR /uniparc_downloader
RUN pip install requests
RUN pip install argparse
ENTRYPOINT [ "python","uniparc_downloader.py"]