FROM ubuntu:22.04
# but youu be aware... I USE ARTIX BTW...
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
# I dont see no sudo nowhere??? Do You...?
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

