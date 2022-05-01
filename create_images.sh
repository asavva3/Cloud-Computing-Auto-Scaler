#!/bin/bash
container=$(buildah from alpine)
buildah run $container -- apk update
buildah run $container -- apk add python3
buildah run $container -- apk add py3-pip
buildah run $container -- pip3 install flask flask_restful flask_limiter --ignore-installed
buildah copy $container objst.py
buildah run $container -- mkdir data
buildah commit $container webapp
buildah config --cmd "" $container
buildah config --entrypoint "python3 objst.py 5 10 15" $container
buildah commit $container webapp

hap=$(buildah from alpine)
buildah run $hap -- apk update
buildah run $hap -- apk add haproxy
buildah copy $hap haproxy.cfg /etc/haproxy/haproxy.cfg
buildah config --cmd "" $hap
buildah config --entrypoint "haproxy -f /etc/haproxy/haproxy.cfg" $hap
buildah commit $hap haproxyimg


wa=$(buildah from alpine)
buildah run $wa -- apk update
buildah run $wa -- apk add python3
buildah copy $wa wait.py
buildah config --cmd "" $wa
buildah config --entrypoint "python3 wait.py" $wa
buildah commit $wa wait


buildah rename $container webappcontainer
buildah rename $hap haproxycontainer
buildah rename $wa waitcontainer