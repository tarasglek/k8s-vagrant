#!/usr/bin/python
import re
import sys
import subprocess
import os
import os.path
import socket

def run(cmd):
    print (cmd)
    sys.stdout.flush()
    return subprocess.check_output(cmd, shell=True)

def get_ip():
    ifconfig = run("ifconfig")
    matches = re.findall(r'^(\S+).*?inet addr:(\S+)', ifconfig, re.S | re.M)
    for m in matches:
        if m[0] == "enp0s8":
            return m[1]
    raise KeyError

def k8s_config():
    run("/vagrant/k8s_config.sh")

def init_save_kube_join_string(filename, ip):
    print run("kubeadm init --apiserver-advertise-address 192.168.50.4 --pod-network-cidr 10.244.0.0/16")
    print run("mkdir -p ~/.kube && cp /etc/kubernetes/admin.conf ~/.kube/config")
    print run("cp /etc/kubernetes/admin.conf /vagrant/config")
    k8s_config()
    #get us a token for worker nodes
    s = run("kubeadm token list")
    #skip header, grab first token
    token = s.split("\n")[1].split(' ')[0]
    join_str = "kubeadm join --token %s %s:6443\n" % (token, ip)
    write_file(filename, join_str)

def write_file(filename, body):
    with open(filename, 'w') as outfile:
        outfile.write(body)
    print "Wrote " + filename

def read_file(filename):
    return open(filename).read()

def mod_kubelet(myip):
    cfg = "\n[Service]\nEnvironment=\"KUBELET_EXTRA_ARGS=--node-ip=%s --enable-controller-attach-detach=false\"\n" % myip
    write_file(
        "/etc/systemd/system/kubelet.service.d/15-node-override.conf", cfg)
    run("systemctl daemon-reload")

"""
Setup first node we run as master. Have rest join it
"""
def init_or_join(filename, myip):
    if socket.gethostname() == "k8s-master":
        init_save_kube_join_string(filename, myip)
    else:
        print run(open(filename).read())

#consistent iscsi IQN
def fix_iscsi_iqn(ip):
    template = "InitiatorName=iqn.1993-08.org.debian:01:7c276e15bd7d"
    ipstr = ip.replace(".", "")
    iqn = template[0:len(template) - len(ipstr)] + ipstr
    write_file("/etc/iscsi/initiatorname.iscsi", iqn)
    run("apt-get install -y open-iscsi")

def main():
    ip = get_ip()
    fix_iscsi_iqn(ip)
    mod_kubelet(ip)
    init_or_join("/vagrant/kubeadm_join", ip)

main()
