FROM centos:7
RUN yum update -y && yum install -y \
  openssh-server \
  passwd
RUN mkdir /var/run/sshd
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N ''
RUN useradd user
RUN echo -e "pass\npass" | (passwd --stdin user)
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
