FROM python:3.9 

ADD . .
RUN pip install discord xdice
CMD ["python", "./main.py"] 