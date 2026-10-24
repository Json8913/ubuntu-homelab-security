#!/usr/bin/env bash
# Read-only snapshot of basic host and service exposure indicators.

set -u

echo "== Host =="
hostname
. /etc/os-release && echo "$PRETTY_NAME"

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
