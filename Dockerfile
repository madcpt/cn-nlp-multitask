FROM python:3.8.10
RUN apt update && apt install -y git-lfs
ADD .git /.git
RUN git lfs pull -I saved_model.zip
RUN unzip saved_model.zip
ADD requirements.txt /
RUN pip3 install numpy==1.23.2
RUN pip install -r requirements.txt
ADD data /data
ADD app.py /
ADD nlp_api.py /
ADD model /model
CMD uvicorn app:app --port 8080 --host 0.0.0.0
