#!/bin/sh
set -x -e
echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDrh16eSSa8gieQlOcmkQZMTWyjdXXezph/MwsSypml62f8qDgEjXSNuFibr58JtWgODFkvj0G3yPVfUIjzdK1dt9oGNBpghX+HHtWMI5XaQz3Fl8dp/mUNL3Qy3wvbWuw4hhv8GnVyGe/y56nJrxcRT3wzXUcpI13NPGTZAhJ8nMXeZWfx3QFGui7dych4WQPmRpyUlbJeDUwzi4GJNSorSUl7Jnos4uYTxdShN6q1SVCKv9kI1tARLIP1422ic3dFWGIbw1p6eW3BBKN4crGSoDzdU1O9Ax6oXtfRZgGEQ6s3oFBzjPJkUUH9Yk//gKxJU9VkLxwtjg/Iv0U+ZmIp taras@taras-mbp >> /root/.ssh/authorized_keys

# ip route add 192.168.50.0/8 dev enp0s8
# save the debs
mkdir -p /vagrant/apt-cache/
rm -rf /var/cache/apt/archives/
ln -sv /vagrant/apt-cache/ /var/cache/apt/archives

if [ ! -f /usr/bin/kubeadm ]; then

  apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl linux-image-extra-$(uname -r) \
    xfsprogs multipath-tools util-linux socat python 

  # instructions cut/pasted from https://kubernetes.io/docs/getting-started-guides/kubeadm/
  curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

  echo deb http://apt.kubernetes.io/ kubernetes-xenial main > /etc/apt/sources.list.d/kubernetes.list

  apt-get update
  # Install docker if you don't have it already.
  apt-get install -y docker.io kubelet kubeadm kubectl kubernetes-cni

fi

#do kubeadm
/vagrant/swap_etc_hosts_run_kubeadm.py
