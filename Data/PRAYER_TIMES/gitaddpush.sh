#!/bin/bash

# Generate a commit message with the current date and "monthly load"
commit_message="$(date +'%Y-%m-%d') - Monthly Load"

# Stage all changes
git add .

# Commit with the generated message
git commit -m "$commit_message"

# Push to the remote repository (assuming you're pushing to the 'origin' branch)
git push origin master

# You can change 'master' to the branch you want to push to if it's different

echo "Git add and push completed."
