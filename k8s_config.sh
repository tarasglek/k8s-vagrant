set -x -e
# flannel rbac
kubectl create -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel-rbac.yml

export VAGRANT_SUFFIX=
if [ -f /vagrant ]; then
    VAGRANT_SUFFIX=-vagrant
fi
kubectl create -f `dirname $0`/kube-flannel${VAGRANT_SUFFIX}.yml
# tiller rbac:
kubectl create -f https://gist.githubusercontent.com/groundnuty/fa778fc06cd79f4de687490afb6de421/raw/b43e3a4c1f2670f038db9415cc7f90b2efd3eab5/serviceaccount_fix.yaml
set +e
# enable scheduling pods on master node
kubectl taint nodes --all node-role.kubernetes.io/master-
