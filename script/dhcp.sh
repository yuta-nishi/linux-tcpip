#!/bin/bash

set -Ceuo pipefail

: "start" && {
    echo "start"
}

: "add-netns" && {
    ip netns add server
    ip netns add client
}

: "add-veth" && {
    ip link add s-veth0 type veth peer name c-veth0
}

: "set-veth" && {
    ip link set s-veth0 netns server
    ip link set c-veth0 netns client
}

: "set-mac-addr" && {
    ip netns exec server ip link set dev s-veth0 address 00:00:5E:00:53:01
    ip netns exec client ip link set dev c-veth0 address 00:00:5E:00:53:02
}

: "link-up" && {
    ip netns exec server ip link set s-veth0 up
    ip netns exec client ip link set c-veth0 up
}

: "add-ip" && {
    ip netns exec server ip address add 192.0.2.254/24 dev s-veth0
}

: "done" && {
    echo "done"
}
