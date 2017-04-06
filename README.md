
`vagrant up`

`cp config /Users/taras/.kube/config`

```
kubectl get --all-namespaces pods -o wide
NAMESPACE     NAME                                 READY     STATUS                                                                                                                                                                                                                                                                                RESTARTS   AGE       IP             NODE
kube-system   etcd-k8s-master                      1/1       Running                                                                                                                                                                                                                                                                               0          6m        192.168.50.4   k8s-master
kube-system   kube-apiserver-k8s-master            1/1       Running                                                                                                                                                                                                                                                                               0          5m        192.168.50.4   k8s-master
kube-system   kube-controller-manager-k8s-master   1/1       Running                                                                                                                                                                                                                                                                               0          7m        192.168.50.4   k8s-master
kube-system   kube-dns-3913472980-q9d0c            0/3       rpc error: code = 2 desc = failed to start container "e6805a7e3767307b063ad682f6b0a46a5a6b0380d7fa7f0b1091478f7847ce03": Error response from daemon: {"message":"cannot join network of a non running container: 068fe6b2b2bc675bececf9ef8d6442180bf5f28fbed4172f58e6b22bddf0250a"}   0          7m        <none>         k8s-master
kube-system   kube-flannel-ds-8jqzg                2/2       Running                                                                                                                                                                                                                                                                               2          1m        192.168.50.5   k8s-node5
kube-system   kube-flannel-ds-sn7sn                2/2       Running                                                                                                                                                                                                                                                                               1          7m        192.168.50.4   k8s-master
kube-system   kube-proxy-2h5bl                     1/1       Running                                                                                                                                                                                                                                                                               0          1m        192.168.50.5   k8s-node5
kube-system   kube-proxy-3847z                     1/1       Running                                                                                                                                                                                                                                                                               0          7m        192.168.50.4   k8s-master
kube-system   kube-scheduler-k8s-master            1/1       Running                                                                                                                                                                                                                                                                               0          7m        192.168.50.4   k8s-master
```

`kubectl logs $(kubectl get pods --all-namespaces | grep api | awk '{print $2}') --namespace=kube-system > logs/apiserver.log`