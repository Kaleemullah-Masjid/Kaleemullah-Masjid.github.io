import subprocess
import os
import datetime
import logging

def main():
    try:
        #Log Start
        logging.info("Update and push Started.")
        #Get today's Date
        cur_date = datetime.date.today()

        # RUN PY SCRIPT
        subprocess.run(["py", ".\get_prayer_times_new.py"])

        # Change the current working directory to the parent directory
        # Get the current working directory
        current_directory = os.getcwd()
        # Get the parent directory's path
        parent_directory = os.path.dirname(current_directory)
        parent_directory = os.path.dirname(parent_directory)
        os.chdir(parent_directory)

        # Run Git commands
        subprocess.run(["git", "pull"])
        # Add the file
        subprocess.run(["git", "add", '.'])

        # Commit the changes
        commit_message = f'Data updated on {cur_date}'
        subprocess.run(["git", "commit", "-m", commit_message])

        # Push to the repository
        subprocess.run(["git", "push"])

        #Log Push
        logging.info("Update and push successful.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error: {e}")
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    # Configure logging
    log_file = './logs/update_log.txt'
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()