FROM python:3.8-alpine
WORKDIR /taxi-booking
ADD . /taxi-booking
RUN pip install -r requirements.txt
CMD ["python","run.py"]