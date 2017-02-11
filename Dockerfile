FROM python:2.7
RUN pip install boto3
RUN pip install nvidia-ml-py
CMD python /main.py
ENV LD_LIBRARY_PATH /usr/lib64
COPY main.py /main.py
