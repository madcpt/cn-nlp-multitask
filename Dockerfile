FROM python:3.8.10
ADD saved_model.zip /
RUN unzip saved_model.zip
ADD requirements.txt /
RUN pip3 install numpy
RUN pip install -r requirements.txt
ADD data /data
ADD app.py /
ADD model.py /
CMD uvicorn app:app --port 8001 --host 0.0.0.0
