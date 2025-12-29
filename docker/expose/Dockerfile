FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends openssh-server \
  && rm -rf /var/lib/apt/lists/* && mkdir -p /var/run/sshd
RUN useradd -m -s /bin/bash user && echo 'user:pass' | chpasswd
RUN ssh-keygen -A
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]
