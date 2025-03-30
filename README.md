# AI Resume Generator

This project is a web-based AI Resume Generator built using Flask. It allows users to input their details, and then it generates a professionally formatted resume in DOCX and PDF formats. Additionally, the app integrates an AI-powered recommendation feature that suggests additional job responsibilities, activities, or related skills based on user input.

## Features

- **Dynamic Resume Generation:**  
  Merge user input into a DOCX template using `docxtpl`, and generate a final resume.

- **Live PDF Preview:**  
  Convert the generated DOCX to a PDF on the fly using LibreOffice in headless mode, and display the preview in the browser via an `<iframe>`.

- **AI Recommendations:**  
  Integrate a free text generation API (e.g., TextGen API) to provide dynamic recommendations for job responsibilities and additional skills based on user-provided experience and skills.

- **Real-Time Updates:**  
  As users type in the form fields, the PDF preview updates live with a debounce mechanism to optimize performance.

## Requirements

### Python Packages

- Flask
- docxtpl
- requests

These packages are listed in the `requirements.txt` file.

### External Dependencies

- **LibreOffice:**  
  The application uses LibreOffice (in headless mode) to convert DOCX files to PDF. You must install LibreOffice manually on your system.  
  **Windows Example:**  
  Install LibreOffice and note its installation path (typically `C:\Program Files\LibreOffice\program\soffice.exe`).  
  Update the `LIBREOFFICE_PATH` variable in the `app.py` file accordingly.

## Setup

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
