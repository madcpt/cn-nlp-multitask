FROM python
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD data /data
ADD app.py /
CMD uvicorn app:app --port 8001 --host 0.0.0.0
