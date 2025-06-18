# H5P to Desktop App

This project converts H5P content into desktop applications, utilizing the SCORM H5P wrapper for packaging H5P files.

## Prerequisites

Before running this project, you need to set up the required dependencies and the SCORM H5P wrapper service.

### System Requirements

- Python 3.7 or higher
- Node.js and NPM
- Git

## Setup Instructions

### 1. Set up the SCORM H5P Wrapper (Required Dependency)

This project depends on the SCORM H5P wrapper service to function properly. Follow these steps to set it up:

#### Repository

```
https://github.com/sr258/scorm-h5p-wrapper.git
```

#### Installation Steps

1. **Install Node.js and NPM** on your system if you haven't already

   - Download from: https://nodejs.org/

2. **Clone the SCORM H5P wrapper repository**

   ```bash
   git clone https://github.com/sr258/scorm-h5p-wrapper.git
   cd scorm-h5p-wrapper
   ```

3. **Install dependencies**

   ```bash
   npm install
   ```

4. **Copy H5P standalone files**

   ```bash
   npm run copy-h5p-standalone
   ```

5. **Start the SCORM H5P wrapper service**
   ```bash
   PORT=8080 npm start
   ```

The SCORM H5P wrapper service will be available at `http://localhost:8080`

### 2. Set up This Project

1. **Clone this repository**

   ```bash
   git clone git@github.com:starkbaknet/h5p-to-desktop-app.git
   cd h5p-to-desktop-app
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   On macOS/Linux:

   ```bash
   source venv/bin/activate
   ```

   On Windows:

   ```bash
   venv\Scripts\activate
   ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

1. **Ensure the SCORM H5P wrapper is running**

   - Make sure you have completed the SCORM H5P wrapper setup above
   - The service should be running on `http://localhost:8080`

2. **Activate your virtual environment** (if not already activated)

   ```bash
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Run the main application**
   ```bash
   python main.py
   ```

## Project Structure

```
h5p-to-desktop-app/
├── generated/          # Generated desktop applications (ignored by git)
├── venv/              # Virtual environment (ignored by git)
├── main.py            # Main application entry point
├── requirements.txt   # Python dependencies
├── .gitignore        # Git ignore file
└── README.md         # This file
```

## About the SCORM H5P Wrapper

The SCORM H5P wrapper is a NodeJS application that packs H5P content into SCORM objects. This project uses it to:

- Convert H5P files into SCORM-compatible packages
- Enable H5P content to work in any LMS that supports SCORM
- Report scores to LMS through SCORM
- Work offline without relying on external H5P sites

For more information about the SCORM H5P wrapper, visit: https://github.com/sr258/scorm-h5p-wrapper
