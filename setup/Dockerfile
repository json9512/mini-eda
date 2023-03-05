FROM python:3.9

RUN apt-get update -y && apt-get install zip unzip sudo -y
RUN adduser --disabled-password --gecos "" user  \
    && echo 'user:user' | chpasswd \
    && adduser user sudo \
    && echo 'user ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN sudo ./aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD python3 setup.py 
