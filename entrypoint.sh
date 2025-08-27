#!/bin/sh
set -e

# Change ownership of mounted volumes to the appuser.
# This allows the non-root user to write to host-mounted directories.
chown -R appuser:appuser /app/data

# Drop privileges and execute the main command (CMD) as the non-root user.
exec gosu appuser "$@"