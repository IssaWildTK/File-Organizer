import json
import os
import shutil
import sys
import logging
import argparse

# Default log directory and file name
DEFAULT_LOG_DIR = "logs"
LOG_FILE_NAME = "file_organizer.log"

# Parse the command-line arguments
parser = argparse.ArgumentParser(description="Organize files into folders and manage logs.")
parser.add_argument('path', nargs='?', default=None, help="The path of the directory to organize. Optional if --cd is "
                                                          "used.")
parser.add_argument('--cd', action='store_true', help="Use the current directory for file organization. No need to "
                                                      "specify a path.")
parser.add_argument('--dry-run', action='store_true', help="Run the script in dry run mode without moving files.")
parser.add_argument('--clear-logs', action='store_true', help="Clear the log files.")
parser.add_argument('--log-dir', default=DEFAULT_LOG_DIR, help="Specify a custom directory for log files.")
args = parser.parse_args()

# Define LOG_FILE_PATH based on the provided log directory
LOG_FILE_PATH = os.path.join(args.log_dir, LOG_FILE_NAME)

# Ensure the logs directory exists before setting up logging or attempting to clear logs
if not os.path.exists(args.log_dir):
    os.makedirs(args.log_dir)


# Define the FileOrganizer class

class FileOrganizer:
    # Initialize the FileOrganizer class
    def __init__(self, path, dry_run=False):
        # Set the path to the provided path or the current working directory
        self.path = path if path else os.getcwd()
        # Get the list of files in the directory
        self.files = os.listdir(self.path)
        # Load the configuration from config.json
        with open('config.json', 'r') as config_file:
            self.config = json.load(config_file)
        # Set the dry_run attribute based on the provided argument
        self.dry_run = dry_run

        # Ensure the logs directory exists
        if not os.path.exists(args.log_dir):
            os.makedirs(args.log_dir)

        # Define LOG_FILE_PATH based on the provided log directory
        global LOG_FILE_PATH
        LOG_FILE_PATH = os.path.join(args.log_dir, LOG_FILE_NAME)

        # Set up logging
        logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info('File organizer started.')

    # Create folders based on the configuration
    def create_folders(self):
        print(f'Organizing files in {self.path}.')
        # Create a unique set of folders based on config.json to ensure no duplicates
        unique_folders = set(self.config.values())
        for folder in unique_folders:
            folder_path = os.path.join(self.path, folder)
            if not os.path.exists(folder_path):
                if not self.dry_run:
                    os.makedirs(folder_path)
                    logging.info(f'Folder created: {folder}')
                else:
                    logging.info(f'Would create folder: {folder}')

    # Move files to the appropriate folders based on the configuration
    def move_files(self):
        # Iterate through the files and move them to the appropriate folders
        for file in self.files:
            file_extension = file.split('.')[-1].lower()
            destination_folder = self.config.get(file_extension, 'Others')
            source_file_path = os.path.join(self.path, file)
            destination_folder_path = os.path.join(self.path, destination_folder)

            if not self.dry_run:
                try:
                    shutil.move(source_file_path, destination_folder_path)
                    logging.info(f'Moved {file} to {destination_folder}.')
                except Exception as e:
                    logging.error(f'Error moving {file} to {destination_folder}: {e}')
            else:
                logging.info(f"Would move {file} to {destination_folder}.")

    # Organize the files in the directory
    def organize(self):
        self.create_folders()
        self.move_files()
        logging.info('File organization complete.')
        print(f"File organization complete. Logs available at {LOG_FILE_PATH}.")

    # Clear the log files
    @staticmethod
    def clear_logs():
        # Use the global LOG_FILE_PATH variable
        try:
            os.remove(LOG_FILE_PATH)
            print(f"Logs cleared successfully from {LOG_FILE_PATH}.")
        except FileNotFoundError:
            print("Log file not found, nothing to clear.")
        except Exception as e:
            print(f"Error clearing logs: {e}")


if __name__ == '__main__':
    # Clear logs if --clear-logs is specified and exit
    if args.clear_logs:
        FileOrganizer.clear_logs()
        sys.exit()

    path = os.getcwd() if args.cd else args.path

    # Proceed with file organization
    if path:
        organizer = FileOrganizer(path, dry_run=args.dry_run)
        organizer.organize()
    else:
        print("Error: Please specify a path, or use --cd to use the current directory.")
        sys.exit(1)