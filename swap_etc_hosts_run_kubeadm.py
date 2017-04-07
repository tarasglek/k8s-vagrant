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

def init_save_kube_join_string(filename, ip):
    print run("kubeadm init --apiserver-advertise-address 192.168.50.4 --pod-network-cidr 10.244.0.0/16")
    print run("mkdir -p ~/.kube && cp /etc/kubernetes/admin.conf ~/.kube/config && cp -R /root/.kube/ ~ubuntu/.kube/ && chown ubuntu:ubuntu -R ~ubuntu/.kube/")
    print run("cp /root/.kube/config /vagrant/config")
    # flannel rbac
    print run("kubectl create -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel-rbac.yml")
    print run("kubectl create -f /vagrant/kube-flannel.yml")
    #print run("kubectl apply -f https://git.io/weave-kube-1.6")
    #enable scheduling pods on master node
    print run("kubectl taint nodes --all node-role.kubernetes.io/master-")
    # to make tiller work:
    print run("curl https://gist.githubusercontent.com/groundnuty/fa778fc06cd79f4de687490afb6de421/raw/b43e3a4c1f2670f038db9415cc7f90b2efd3eab5/serviceaccount_fix.yaml  | kubectl create -f -")

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
    mod_kubelet(myip)
    if socket.gethostname() == "k8s-master":
        init_save_kube_join_string(filename, myip)
    else:
        print run(open(filename).read())

def main():
    ip = get_ip()
    #consistent iscsi IQN
    # template = "InitiatorName=iqn.1993-08.org.debian:01:7c276e15bd7d"
    # id = ip.replace(".", "")
    # iqn = template[0:len(template) - len(id)] + id
    # write_file("/etc/iscsi/initiatorname.iscsi", iqn)
    # run("systemctl restart open-iscsi")
    init_or_join("/vagrant/kubeadm_join", ip)

main()
