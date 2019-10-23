FROM python:3.7.5-alpine3.9
COPY . /google_calendar_schedule
WORKDIR /google_calendar_schedule
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["startup.py"]
