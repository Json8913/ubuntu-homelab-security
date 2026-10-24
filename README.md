# Ubuntu Server Home Lab Security

A growing set of notes for documenting a small Ubuntu Server home lab running Jellyfin, with a read-only script for checking basic host and service exposure indicators.

**Stage:** Initial notes and read-only check. This repository does not claim that a server has been deployed or independently assessed.

## Baseline checklist

- Keep Ubuntu packages updated and remove services that are not needed.
- Use a non-root administrator account and SSH keys.
- Restrict SSH and Jellyfin access to the intended local network.
- Enable and review the host firewall before exposing any service.
- Keep Jellyfin and other services updated.
- Back up configuration and media metadata, then document a restore procedure.
- Review listening ports and service logs after configuration changes.

## Read-only check

Run:

    bash baseline_check.sh

The script reports the operating system, UFW status, listening sockets, and Jellyfin service state. It does not change system configuration. Its output can contain host and network details; redact it before sharing.

## Validation

The script passed a Bash syntax check. Run it on the Ubuntu Server you intend to document; its output describes the machine where it is run.

## Documentation plan

Record the server version, network diagram, firewall rules, service exposure, update process, backup approach, and lessons learned. Do not publish public IP addresses, hostnames, credentials, or private logs.

## Screenshots

Add redacted screenshots of the local dashboard and firewall status after the lab is configured.
