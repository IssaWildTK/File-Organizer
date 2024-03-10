import json
import os
import shutil
import sys
import logging
import argparse

# Default log directory and file name
DEFAULT_LOG_DIR = "logs"
LOG_FILE_NAME = "file_organizer.log"


class FileOrganizer:
    def __init__(self, path, dry_run=False):
        self.path = path if path else os.getcwd()
        self.files = os.listdir(self.path)
        with open('config.json', 'r') as config_file:
            self.config = json.load(config_file)
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

    def create_folders(self):
        print(f'Organizing files in {self.path}.')
        unique_folders = set(self.config.values())
        for folder in unique_folders:
            folder_path = os.path.join(self.path, folder)
            if not os.path.exists(folder_path):
                if not self.dry_run:
                    os.makedirs(folder_path)
                    logging.info(f'Folder created: {folder}')
                else:
                    logging.info(f'Would create folder: {folder}')

    def move_files(self):
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

    def organize(self):
        self.create_folders()
        self.move_files()
        logging.info('File organization complete.')
        print(f"File organization complete. Logs available at {LOG_FILE_PATH}.")

    @staticmethod
    def clear_logs():
        try:
            os.remove(LOG_FILE_PATH)
            print(f"Logs cleared successfully from {LOG_FILE_PATH}.")
        except FileNotFoundError:
            print("Log file not found, nothing to clear.")
        except Exception as e:
            print(f"Error clearing logs: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Organize files into folders and manage logs.")
    parser.add_argument('path', nargs='?', default=None,
                        help="The path of the directory to organize. Optional if --cd is used.")
    parser.add_argument('--cd', action='store_true',
                        help="Use the current directory for file organization. No need to specify a path.")
    parser.add_argument('--dry-run', action='store_true', help="Run the script in dry run mode without moving files.")
    parser.add_argument('--clear-logs', action='store_true', help="Clear the log files.")
    parser.add_argument('--log-dir', default=DEFAULT_LOG_DIR, help="Specify a custom directory for log files.")
    args = parser.parse_args()

    # Clear logs if --clear-logs is specified and exit
    if args.clear_logs:
        FileOrganizer.clear_logs()
        sys.exit()

    # Proceed with file organization
    organizer = FileOrganizer(args.path, dry_run=args.dry_run)
    organizer.organize()
