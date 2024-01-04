#!/bin/bash

# Replace these variables with your own values
BUCKET="your-spaces-bucket-name"
REGION="your-spaces-region"  # e.g., nyc3
MOUNT_POINT="/path/to/mount/point"
ACCESS_KEY="your-spaces-access-key"
SECRET_KEY="your-spaces-secret-key"

# Construct the DigitalOcean Spaces endpoint
ENDPOINT="https://${REGION}.digitaloceanspaces.com"

# Check if the mount point exists, create if not
if [ ! -d "$MOUNT_POINT" ]; then
  mkdir -p "$MOUNT_POINT"
fi

# Mount the DigitalOcean Spaces bucket using s3fs
s3fs "$BUCKET" "$MOUNT_POINT" -o passwd_file <(echo "$ACCESS_KEY:$SECRET_KEY") -o url="$ENDPOINT"

# Check if the mount was successful
if [ $? -eq 0 ]; then
  echo "OVH Object Storage bucket mounted successfully at $MOUNT_POINT"
else
  echo "Failed to mount OVH Object Storage bucket"
fi
