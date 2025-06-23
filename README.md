# Portarias Search Application - Detailed Guide

## Overview

This application is designed to search for "portarias" (official administrative documents) from the "Ministério Público de Contas do Estado do Pará" (MPC-PA). It automates the process of downloading PDFs from the MPC-PA website, extracting text from these PDFs, and storing the extracted text in a CouchDB database. A Vue.js-based frontend provides a user interface to search and view these documents.

## System Architecture

The application consists of the following main components:

1.  **PDF Downloader (Python):** Downloads PDF files from the MPC-PA website.
2.  **PDF Processor (Python):** Extracts text content from the downloaded PDFs using OCR (Optical Character Recognition) if necessary.
3.  **CouchDB Uploader (Python):** Uploads the extracted text data into a CouchDB database.
4.  **CouchDB:** A NoSQL database used to store the extracted text and metadata.
5.  **Frontend (Vue.js):** A web-based user interface for searching and displaying the "portarias".
6.  **Nginx:** A web server that serves the frontend application and proxies requests to the CouchDB database.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Docker:** Docker is required to containerize and run the application.
*   **Docker Compose:** Docker Compose is used to define and manage multi-container Docker applications.

## Setup and Installation

Follow these steps to set up and run the application:

1.  **Clone the Repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Environment Configuration:**

    *   Create a `.env` file in the project root directory.
    *   Configure the necessary environment variables:

        ```
        NODE_ENV=development
        HOST=0.0.0.0
        PORT=3000
        VITE_COUCHDB_URL=http://localhost:5984
        COUCHDB_USER=admin
        COUCHDB_PASSWORD=mpc123
        COUCHDB_SECRET=development_secret
        ```

        *   `NODE_ENV`: Set the environment to `development` or `production`.
        *   `HOST`: The host address for the frontend application.
        *   `PORT`: The port number for the frontend application.
        *   `VITE_COUCHDB_URL`: The URL for the CouchDB database.
        *   `COUCHDB_USER`: The CouchDB admin username.
        *   `COUCHDB_PASSWORD`: The CouchDB admin password.
        *   `COUCHDB_SECRET`: A secret key for CouchDB.

3.  **Run the Application:**

    *   Start the application using Docker Compose:

        ```bash
        docker-compose up -d
        ```

        This command builds the Docker images and starts the containers in detached mode.

## Accessing the Application

Once the application is running, you can access it via your web browser at:

```
http://localhost:3000
```

## Application Components - Details

### 1. Python Scripts

The python scripts are located in the `src/python` directory.

*   **pdf\_downloader.py:**
    *   Downloads PDF files from a specified URL.
    *   Extracts links to PDF documents from the specified webpage.
    *   Downloads the PDF files to the designated output directory.
*   **pdf\_processor.py:**
    *   Processes PDF files to extract text content.
    *   Uses `PyMuPDF` to open and read PDF files.
    *   If direct text extraction fails, it uses `pytesseract` for OCR (Optical Character Recognition).
*   **db\_uploader.py:**
    *   Manages the CouchDB database.
    *   Includes functions to create, delete, and upload documents to the CouchDB database.
    *   Supports batch uploading of documents for efficiency.
*   **main.py:**
    *   Main script to orchestrate the entire process.
    *   Downloads PDFs, processes them, and uploads the extracted text to CouchDB.
    *   Handles logging and error management.

### 2. Docker Configuration

*   **Dockerfile:**
    *   Defines the steps to build the Docker image for the frontend application.
    *   Uses a multi-stage build process to optimize the image size.
    *   Installs dependencies, copies the application code, and builds the frontend.
*   **Dockerfile.couchdb:**
    *   Defines the steps to set up the CouchDB Docker image.
    *   Configures environment variables for CouchDB.
*   **docker-compose.yml:**
    *   Defines the services, networks, and volumes for the application.
    *   Configures the relationships and dependencies between the services.

### 3. Frontend (Vue.js)

*   **src/App.vue:**
    *   Main component that defines the layout and structure of the application.
    *   Includes the header, search bar, and portarias list.
*   **src/components/\*:**
    *   Reusable Vue.js components for the application.
    *   Includes components for the search bar, portarias list, loading spinner, and error messages.
*   **src/stores/portariaStore.js:**
    *   Pinia store to manage the state of the application.
    *   Includes actions to search portarias, load tags, and manage the selected tags.
*   **src/services/couchdbService.js:**
    *   Service to interact with the CouchDB database.
    *   Includes functions to search portarias and retrieve individual portarias.

### 4. Nginx Configuration

*   **nginx.conf:**
    *   Configures the Nginx web server to serve the frontend application.
    *   Sets up reverse proxy rules to forward requests to the CouchDB database.
    *   Configures CORS (Cross-Origin Resource Sharing) to allow requests from the frontend to the CouchDB database.

## Updating the Database

To update the database with the latest "portarias", follow these steps:

1.  Ensure the application is running.
2.  Access the Docker container for the `python-updater` service:

    ```bash
    docker exec -it <python-updater_container_id> bash
    ```

3.  Run the `main.py` script:

    ```bash
    python main.py
    ```

    This script will download the latest PDFs, extract the text, and update the CouchDB database.

## Development

To run the application in development mode:

1.  Ensure the application is running.
2.  Modify the source code in the `src` directory.
3.  The frontend application will automatically reload when changes are made to the source code.

## Volumes

The following volumes are used to persist data:

*   `couchdb_data`: Persists CouchDB data.
*   `couchdb_config`: Stores CouchDB configuration.
*   `python_data`: Stores downloaded PDF files.
*   `python_texts`: Stores extracted text files.

## Networks

The application uses a single network:

*   `app-network`: Internal network for service communication.

## Troubleshooting

*   **Application not accessible:**
    *   Ensure that Docker is running.
    *   Check the container logs for any errors.
    *   Verify that the port mappings are correct in the `docker-compose.yml` file.
*   **Database not updating:**
    *   Check the logs for the `python-updater` service for any errors.
    *   Ensure that the CouchDB database is accessible from the `python-updater` container.
    *   Verify that the CouchDB credentials are correct in the `.env` file.

## Additional Information

*   **CouchDB Web Interface:** You can access the CouchDB web interface at `http://localhost:5984` to view and manage the database.
*   **Logging:** The application uses logging to provide information about the system's operation. Check the container logs for details.

This guide should provide you with a comprehensive understanding of the application and how to set it up and run it successfully.
