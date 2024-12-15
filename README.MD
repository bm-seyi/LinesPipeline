# LinesPipeline

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
   - [Prerequisites](#prerequisites)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [License](#license)
7. [Contact](#contact)

## Introduction
LinesPipeline is an Extract, Transform, and Load (ETL) project designed to collect and manage geographical data for the Metrolink network's lines. By leveraging OpenStreetMap APIs, the project retrieves raw geographical data, processes it to ensure accuracy and usability, and loads it into a SQL Server database for efficient storage and access. This streamlined approach facilitates better data management and integration for applications requiring up-to-date geographical information.

## Features
- **Data Retrieval**: Seamlessly fetches geographical data from OpenStreetMap APIs.  
- **Data Transformation**: Cleanses and transforms raw data into a structured format, ready for database integration.  
- **Database Integration**: Loads the processed data into a robust SQL Server database for secure and scalable storage.  
- **Extensibility**: Built to accommodate future enhancements, such as additional data sources or expanded network coverage.  
- **Automation**: Fully automated pipeline for minimal manual intervention and consistent data updates.  

## Installation

### Prerequisites
- **Python 3.10 or later**: Ensure that Python 3.10 or a later version is installed on your system.

- **Required Python Packages**: Install the necessary Python packages by running the following command:

    ```bash
    pip install -r requirements.txt
    ```

## Usage
To run the project, you can either:

- **Windows**: Double-click the `run.bat` file in File Explorer.
- **Other OS**: Execute the `__main__.py` file directly.

## Configuration
To run this project, add the following environment variables to a `.env` file stored in the root directory:

    ```
    connString = "your connection string"
    ```

## License
This project is licensed under the MIT License. For more details, see the LICENSE file.
