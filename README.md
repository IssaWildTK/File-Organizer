# Python Automated File Organizer

The Python File Organizer is a powerful tool designed to automate the process of sorting and organizing files within a specified directory. It categorizes files into designated folders based on their file type, streamlining your digital workspace and making it easier to manage large volumes of files.

## Features

- **Automated File Sorting**: Moves files into categorized folders based on file extensions.
- **Customizable Configuration**: Easily modify file type-to-folder mappings through `config.json`.
- **Logging**: Detailed logging of file movements and errors for easy tracking and debugging.
- **Dry Run Option**: Preview file organization actions without making any changes.
- **Custom Log Directory**: Specify a custom directory for log files or use the default.

## Getting Started

### Prerequisites

Ensure you have Python 3.x installed on your system. This project does not require any external dependencies beyond the standard library.

### Installation

1. Clone the repository to your local machine:
    
    ```bash
    git clone https://github.com/IssaWildTK/File-Organizer.git
    ```
2. Navigate to the project directory:
    
        
        cd File-Organizer
   

### Usage

To organize files in a directory, run the script with the path to the target directory:
    
    organize.py /path/to/directory


#### Dry Run

To simulate the organization process without making any changes:
        
        organize.py /path/to/directory --dry-run
        


#### Custom Log Directory

To specify a custom directory for logs:
            
            organize.py /path/to/directory --log-dir /path/to/log/directory
            


#### Clearing Log Files

To clear existing log files:
                   
                 organize.py /path/to/directory --clear-log
                 


## Configuration

Modify `config.json` to change the mapping of file extensions to folder names according to your preferences.

Example configuration:
```json
{
  "jpg": "Images",
  "png": "Images",
  "txt": "Documents"
  // Add more mappings as needed
}
```
#### Note: The default config.json file includes a comprehensive set of file extension-to-folder mappings designed to cover a wide range of file types. It's recommended to review and customize this file to fit your specific organizational needs and preferences. Tailoring the configuration ensures that the file organization process aligns closely with your unique workflow and directory structure.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to discuss proposed changes or enhancements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
