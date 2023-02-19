#!/bin/bash

set -Ceuo pipefail

: "start" && {
    echo "start"
}

: "add-netns" && {
    ip netns add ns1
    ip netns add ns2
}

: "add-veth" && {
    ip link add ns1-veth0 type veth peer name ns2-veth0
}

: "set-veth" && {
    ip link set ns1-veth0 netns ns1
    ip link set ns2-veth0 netns ns2
}

: "link-up" && {
    ip netns exec ns1 ip link set ns1-veth0 up
    ip netns exec ns2 ip link set ns2-veth0 up
}

: "add-ip" && {
    ip netns exec ns1 ip address add 192.0.2.1/24 dev ns1-veth0
    ip netns exec ns2 ip address add 192.0.2.2/24 dev ns2-veth0
}

: "test" && {
    ip netns exec ns1 ping -c 3 192.0.2.2 -I 192.0.2.1
}

: "done" && {
    echo "done"
}
