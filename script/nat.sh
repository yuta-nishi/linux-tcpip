#!/usr/bin/env bash

set -Ceuo pipefail

: "start" && {
    echo "start"
}

: "add-netns" && {
    ip netns add lan
    ip netns add router
    ip netns add wan
}

: "add-veth" && {
    ip link add lan-veth0 type veth peer name gw-veth0
    ip link add wan-veth0 type veth peer name gw-veth1
}

: "set-veth" && {
    ip link set lan-veth0 netns lan
    ip link set gw-veth0 netns router
    ip link set gw-veth1 netns router
    ip link set wan-veth0 netns wan
}

: "link-up" && {
    ip netns exec lan ip link set lan-veth0 up
    ip netns exec router ip link set gw-veth0 up
    ip netns exec router ip link set gw-veth1 up
    ip netns exec wan ip link set wan-veth0 up
}

: "setup-lan" && {
    ip netns exec lan ip address add 192.0.2.1/24 dev lan-veth0
    ip netns exec lan ip route add default via 192.0.2.254
}

: "setup-router" && {
    ip netns exec router ip address add 192.0.2.254/24 dev gw-veth0
    ip netns exec router ip address add 203.0.113.254/24 dev gw-veth1
    ip netns exec router sysctl net.ipv4.ip_forward=1
}

: "setup-wan" && {
    ip netns exec wan ip address add 203.0.113.1/24 dev wan-veth0
    ip netns exec wan ip route add default via 203.0.113.254
}

: "add-snat-rule" && {
    ip netns exec router iptables -t nat \
        -A POSTROUTING \
        -s 192.0.2.0/24 \
        -o gw-veth1 \
        -j MASQUERADE
}

: "add-dnat-rule" && {
    ip netns exec router iptables -t nat \
        -A PREROUTING \
        -p tcp \
        --dport 54321 \
        -d 203.0.113.254 \
        -j DNAT \
        --to-destination 192.0.2.1
}

: "test" && {
    ip netns exec lan ping -c 3 203.0.113.1
}

: "done" && {
    echo "done"
}
