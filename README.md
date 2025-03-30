AI Resume Generator
===================

Overview:
---------
The AI Resume Generator is a web-based application built using Flask. It allows users to enter their personal details,
work experience, education, skills, and activities into a form. The application then merges these inputs into a DOCX
template and converts it to PDF for download. In addition, the app uses an AI-powered recommendation feature via a
free text generation API to suggest additional details and improvements based on user input.

Features:
---------
- Dynamic Resume Generation:
  * Merges user input into a DOCX template using docxtpl.
  * Generates a final resume in DOCX and PDF formats.
  
- Live PDF Preview:
  * Converts the DOCX to PDF on the fly using LibreOffice in headless mode.
  * Displays the PDF in an embedded preview (iframe).

- AI Recommendations:
  * Uses a free text generation API to suggest job details, activities, and related skills based on user input.
  * Recommendations are integrated directly into the input section (e.g., when the user enters a skill).

- Real-Time Updates:
  * As the user types, the PDF preview updates automatically.
  * Debounce techniques are used to limit update frequency.

Requirements:
-------------
Python Packages:
  - Flask
  - docxtpl
  - requests

These are listed in the requirements.txt file.

External Dependencies:
  - LibreOffice:
    * Used in headless mode to convert DOCX to PDF.
    * Must be installed on your system.
    * On Windows, ensure LIBREOFFICE_PATH in app.py is set correctly (e.g., 
      C:\Program Files\LibreOffice\program\soffice.exe).

  - Free Text Generation API:
    * The application uses a free text generation API (e.g., TextGen API or similar)
      for AI recommendations.

Installation:
-------------
1. Clone the repository:
   git clone <repository_url>
   cd <repository_directory>

2. Install Python dependencies:
   pip install -r requirements.txt

3. Install LibreOffice:
   - Download and install from https://www.libreoffice.org/download/download/
   - Verify installation and update LIBREOFFICE_PATH in app.py if needed.

4. Prepare the DOCX Template:
   - Place your resume DOCX template in the "template" folder.
   - Ensure merge fields (e.g., {{ NAME }}, {{ EXPERIENCE_1 }}) match the keys used in app.py.

Usage:
------
1. Run the application:
   python app.py

2. Open your browser and navigate to:
   http://127.0.0.1:5000/

3. Fill out the form:
   - Enter your details, experience, education, skills, etc.
   - As you type, the live PDF preview updates automatically.
   - When you leave a skill field, an AI recommendation is triggered and displayed below that field.

4. Generate the resume:
   - Click "Generate Resume" to produce the final DOCX for download.

API Endpoints:
--------------
- "/" (GET, POST):
  * Renders the main form and handles final resume generation.
  
- "/preview_pdf" (POST):
  * Generates a DOCX from the form data, converts it to PDF via LibreOffice,
    and returns the PDF for live preview.

- "/generate_recommendation" (POST):
  * Accepts JSON data (experience and skills), builds a prompt, and returns AI recommendations.

Deployment:
-----------
For production, consider using a WSGI server like Gunicorn and deploying on platforms such as Heroku, AWS,
or DigitalOcean. Ensure proper configuration of environment variables and static file serving.

Troubleshooting:
----------------
- If the DOCX to PDF conversion fails, verify that LibreOffice is installed and LIBREOFFICE_PATH in app.py is correct.
- If the live preview is empty, check that your DOCX template contains valid merge fields and is not empty.
- If AI recommendations do not appear, ensure that your network allows outbound HTTP requests to the text generation API.

License:
--------
This project is provided "as is" without warranty. You are free to modify and distribute it as needed.

Happy Resume Building!
