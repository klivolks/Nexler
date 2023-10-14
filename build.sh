#!/bin/bash

# Define the image name
image_name="docker.io/klivolks/nexler" # your image name

# Get the latest commit SHA
commit_sha=$(git log -1 --pretty=format:"%H")
shortened_sha=$(echo "$commit_sha" | cut -c 1-7)

# Get the current branch name
branch_name=$(git rev-parse --abbrev-ref HEAD)

# Combine branch name and commit hash for the tag
image_tag="$branch_name-$shortened_sha"

# Build the Docker image
echo "Building Docker image..."
docker build -f "DockerfileK8" -t "$image_name:$image_tag" . &

# Display a progress bar
echo -n "["
while :
do
    echo -n "#"
    sleep 1
    if ! ps | grep -q "$!"
    then
        break
    fi
done
echo "]"
echo "Docker image build completed."

# Push the Docker image
echo "Pushing Docker image..."
docker push "$image_name:$image_tag"

echo "Image pushed successfully."

