FROM python:slim
COPY . /dcs-forum
WORKDIR /dcs-forum
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["python", "run.py"]
