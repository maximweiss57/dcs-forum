FROM python
COPY . /DCS-FORUM
WORKDIR /DCS-FORUM
RUN pip install -r requirements.txt
CMD run.py 
