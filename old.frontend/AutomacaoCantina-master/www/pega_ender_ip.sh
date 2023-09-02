#!/bin/bash

environ=${CANTINA}

ifaces=$(cat /proc/net/dev | grep -v lo | awk -F\: '{ if (NF>1) print $1 }')

iface="enp2s0"
iface="wlp2s0"
if [ "$environ" == "" ] ; then
  pi=$(cat /proc/cpuinfo | grep Hardware | grep BCM | wc -l)
  if [ $pi -ne 0 ] ; then
    iface="eth0"
  fi
fi

if [ "$environ" == "controlador-pi" ] ; then
  iface="wlan0"
fi

echo "$0 em $environ" > saida.iface
date >> saida.iface
echo $iface >> saida.iface

#ifconfig $iface | grep inet | grep -v inet6 | awk -v IFACE=$iface '{ n=split ($2, IP, ":") ; if (n > 1) { printf "%s: %s", IFACE, IP[2] } else { printf "%s: %s", IFACE, $2 } }'
ifconfig $iface | grep inet | grep -v inet6 | awk -v IFACE=$iface '{ n=split ($2, IP, ":") ; if (n > 1) { printf "%s: %s", IFACE, IP[2] } else { printf "%s", $2 } }'
