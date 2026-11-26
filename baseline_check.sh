#!/usr/bin/env bash
# Read-only snapshot of basic host and service exposure indicators.

set -u

echo "== Host =="
hostname
if [ -r /etc/os-release ]; then
  . /etc/os-release
  echo "${PRETTY_NAME:-Unknown Linux distribution}"
else
  echo "Operating system details are unavailable"
fi
if [ "$(id -u)" -eq 0 ]; then
  echo "Privilege: running as root"
else
  echo "Privilege: running as a regular user; some process details may be hidden"
fi

echo
echo "== Firewall =="
if command -v ufw >/dev/null 2>&1; then
  ufw status verbose
else
  echo "ufw is not installed"
fi

echo
echo "== Listening sockets =="
if command -v ss >/dev/null 2>&1; then
  ss -lntup
  wildcard_listeners="$(ss -H -lntu 2>/dev/null | awk '$4 ~ /^\*:/ || $4 ~ /^0\.0\.0\.0:/ || $4 ~ /^\[::\]:/ || $4 ~ /^:::/ { print $4 }')"
  if [ -n "$wildcard_listeners" ]; then
    echo
    echo "Review wildcard-bound listeners; they may accept connections on more than one interface:"
    printf '%s\n' "$wildcard_listeners" | sort -u
  else
    echo "No wildcard-bound TCP or UDP listeners were detected"
  fi
else
  echo "ss is not available"
fi

echo
echo "== Jellyfin service =="
if command -v systemctl >/dev/null 2>&1; then
  systemctl is-active jellyfin 2>/dev/null || echo "Jellyfin service is not active or not installed"
else
  echo "systemd is not available"
fi

echo
echo "This script only reports local status; it does not change host configuration."
