import subprocess
import os
import datetime

# Replace these with your own repository information
#repository_url = "https://github.com/yourusername/yourrepository.git"
#file_to_add = "example.txt"
#commit_message = "Added example.txt"
cur_date = datetime.date.today()

print('______STARTED______')
# Get the current working directory
current_directory = os.getcwd()
# Get the parent directory's path
parent_directory = os.path.dirname(current_directory)

# RUN PY FILE
#subprocess.run(["py", ".\get_prayer_times.py"])

# Change the current working directory to the parent directory
os.chdir(parent_directory)

print('______ GIT COMMDS ______')
# Run Git commands
# Add the file
subprocess.run(["git", "add", '.'])

# Commit the changes
subprocess.run(["git", "commit", "-m", f'DATA UPDATED - {cur_date}'])

# Push to the repository
subprocess.run(["git", "push"])
