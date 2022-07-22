FROM python:3.9.6-slim
WORKDIR /app
COPY . ./
RUN pip3 install -r /app/requirements.txt --no-cache-dir
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
