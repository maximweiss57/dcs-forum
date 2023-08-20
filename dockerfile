FROM python:slim
COPY . /DCS-FORUM
WORKDIR /DCS-FORUM
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["python", "run.py"]
