FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apt-get update && apt-get install -y apache2 libapache2-mod-wsgi-py3
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.conf /etc/apache2/sites-available/
RUN a2ensite app.conf
COPY . .
EXPOSE 80
CMD ["apache2ctl", "-D", "FOREGROUND"]
