# Use the official Debian-hosted Python image
FROM python:3.8-slim-buster

# Python wants UTF-8 locale
ENV LANG=C.UTF-8

# Tell Python to disable buffering so we don't lose any logs.
ENV PYTHONUNBUFFERED=1

# Ensure we have an up-to-date baseline, install dependencies, and
# create a user so we don't run the app as root
RUN set -ex; \
  for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done && \
  apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y --no-install-recommends $DEBIAN_PACKAGES && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  pip install --no-cache-dir --upgrade pip && \
  useradd -ms /bin/bash app -d /home/app -u 1000 -p "$(openssl passwd -1 Passw0rd)" && \
  mkdir -p /app && \
  chown app:app /app

# Switch to the new user
USER app
WORKDIR /app

# Copy and install Python packages from requirements.txt
COPY --chown=app:app requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Add the rest of the source code. This is done last so we don't invalidate all
# layers when we change a line of code.
COPY --chown=app:app . /app

ENTRYPOINT ["bash"]

