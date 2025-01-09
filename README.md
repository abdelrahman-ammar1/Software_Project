# Software_Project
# Car Dealership System

This repository contains the implementation and deliverables for the **Car Dealership System** project. The project is structured into milestones to ensure an organized development process. Each milestone contains specific documentation, source code, and supporting materials.

---

## Repository Structure

### **Milestone 1: Project Requirements**
- **Description**: Contains the initial project documentation, including the functional and non-functional requirements, and use case scenarios.
- **Files**:
  - `Milestone_1.pdf`: A detailed description of the project requirements, functional and non-functional requirements, and use case scenarios.

---

### **Milestone 2: Database Design**
- **Description**: Contains the Entity-Relationship Diagram (ERD), relational database schema, and SQL queries for database setup and interaction.
- **Files**:
  - `Milestone_2.pdf`: The Entity-Relationship Diagram and relational database schema used in the system. Also the SQL queries for inserting, updating, deleting, and retrieving data.

---

### **Milestone 3: Webpage Development**
- **Description**: Contains the source code for the web application, including the frontend and backend files, and the original project prompt used for design.
- **Files**:
  - `Prompt`: The original project prompt that guided the webpage design and functionality.
  - `Source_Code/`: A directory containing all the source files used in the web application (HTML, CSS, JavaScript, and Python).

---

### **Milestone 4: Testing and Deployment**
- **Description**: Contains the test cases, defect reports, and automated test scripts used to verify the system's functionality.
- **Files**:
  - `testcases.xlsx`: A spreadsheet with all the manual test cases.
  - `Defect.xlsx`: A spreadsheet will all the defects.
  - `test_cases.robot`: A Robot Framework file automating three critical test cases for the system.

---

## Getting Started

### Prerequisites
To run the project locally, you will need:
- Python with Flask installed
- A local or remote SQL database server (SQL Server was used)
- A web browser for accessing the web application

### **Instructions**

#### **Accessing and Testing the Webpage**

1. **Clone the Repository**
   - Open your terminal or command prompt.
   - Run the following command to clone the repository to your local machine:
     ```bash
     git clone https://github.com/abdelrahman-ammar1/Software_Project.git
     cd Software_Project
     ```

2. **Navigate to the Source Code Directory**
   - Inside the repository folder, locate the `Source_Code/` directory.  
   - This directory contains all the files needed to run the webpage.

3. **Download All Files**
   - Ensure you download the following files from the `Source_Code/` directory:
     - `templates/`: The HTML files for the web application.
     - 'static/': The css and js files
     - 'app.py': Serves as the main application logic for handling routes, connecting to the database, and defining the backend functionality of the website.
     - 'db_config.py': Database connection

4. **Open the Webpage**
   - After downloading all the files, locate the `app.py` file on your local machine.
   - Run the app.py file and choose your preferred browser

5. **Interact with the Webpage**
   - The homepage of the Car Dealership System will load in your browser.
   - Use the webpage to:
     - Log in as a customer, salesperson, or admin.
     - Perform actions such as booking cars, approving bookings, managing inventory, and viewing reports.

---

#### **Additional Notes**
- Ensure that all files from the `Source_Code/` directory are in the same folder on your local machine. Missing files might cause the webpage to malfunction.
- If the webpage does not open or displays incorrectly, verify that your browser is up-to-date.
- The webpage is built with basic HTML, CSS, and JavaScript, so no additional server setup or software installation is required.

