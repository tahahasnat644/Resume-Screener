### Project Description

**Resume Screener Application**

#### Objective
To create an application enabling users to upload resume PDF files, process these files to extract relevant information, and categorize each resume into predefined categories using a machine learning model.

#### Components

1. **Frontend:**
   - **Technology:** React
   - **File:** `FileUpload.js`
   - **Description:**
     - Provides a user interface for uploading resume files.
     - Uses `react-dropzone` for a drag-and-drop file upload area.
     - Users can drag and drop or select PDF files, which are then displayed.
     - An upload button sends the selected files to the backend server.
     - Displays categorization results in a table format after uploading.

2. **Backend:**
   - **Technology:** Flask
   - **File:** `app.py`
   - **Description:**
     - Handles file uploads and processing.
     - Saves uploaded files to an upload directory.
     - Extracts text from PDFs using `PyPDF2`.
     - Cleans and preprocesses the text to isolate qualifications and experiences.
     - Uses a pre-trained machine learning model (saved as `pipeline.joblib`) to predict resume categories.
     - Moves categorized resumes to corresponding directories.
     - Sends categorization results back to the frontend in JSON format.

### Workflow

1. **User Interaction:**
   - Users visit the web interface, drag-and-drop or select resume PDF files.
   - Click the "Upload Files" button to initiate the upload process.

2. **File Handling and Processing:**
   - The frontend sends selected files to the backend server via a POST request.
   - The backend saves the files, extracts, and cleans the text content.
   - The machine learning model categorizes each resume based on the processed text.

3. **Result Display:**
   - The backend returns categorization results to the frontend.
   - The frontend displays these results in a table showing filenames and their categories.

### Key Features

- **Drag-and-Drop File Upload:** An intuitive area for uploading PDF files.
- **File Validation:** Ensures only PDF files are accepted.
- **Text Extraction and Cleaning:** Extracts and cleans text from PDF files.
- **Machine Learning Categorization:** Categorizes resumes using a pre-trained model.
- **Result Visualization:** Displays categorization results in a user-friendly table.
- **Categorized File Storage:** Organizes uploaded resumes into categorized directories.

### Technologies Used

- **Frontend:** React, `react-dropzone`, Axios
- **Backend:** Flask, `PyPDF2`, `scikit-learn`, `joblib`
- **Other Libraries:** `flask-cors` for CORS, `werkzeug` for secure file handling

This project provides a seamless experience for uploading and categorizing resumes, leveraging machine learning for intelligent categorization.

### Execution Instructions

#### Prerequisites
- Node.js and npm installed
- Python and pip installed

#### Frontend (React)

1. **Navigate to the frontend directory:**
   cd path/to/frontend

2. **Install dependencies:**
   npm install

3. **Start the React development server:**
   npm start

#### Backend (Flask)

1. **Navigate to the backend directory:**
   cd path/to/backend

2. **Create a virtual environment and activate it:**
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install dependencies:**
   pip install -r requirements.txt

4. **Ensure the upload folders exist:**
   mkdir -p uploads categorized_pdfs

5. **Run the Flask server:**
   flask run

#### Accessing the Application

1. **Open your browser and navigate to:**
   http://localhost:3000

2. **Use the interface to upload resume PDF files and view the categorization results.**

Ensure both servers are running simultaneously for the application to work correctly. The frontend (React) runs on port 3000, while the backend (Flask) runs on port 5000. Adjust the configurations if necessary.
