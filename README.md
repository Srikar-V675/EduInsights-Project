# EduInsights-Project
**Introduction:** The Comprehensive Student Performance Dashboard integrates advanced data analysis techniques with automation features to provide educators with a powerful platform for analyzing, visualizing, and forecasting student performance data. By combining a single-page application (SPA) architecture with React.js for the frontend and FastAPI for the backend, this dashboard aims to streamline the process of monitoring student progress and making data-driven decisions to support student success.

### **Features:**

1. **Automated PDF Extraction:**
    
    - Automatically extract semester marks from PDF reports stored in a designated Google Drive folder.
    - Convert extracted data into a structured format and calculate total marks, percentage, and SGPA for each student.
2. **Grouped Extractions:**
    
    - Organize extracted data by class or semester, allowing educators to group and access information for specific cohorts.
3. **Visualizations and Analysis:**
    
    - Generate interactive visualizations and analysis on student performance data, including:
        - Distribution of grades
        - Top-performing students
        - Trends over time
        - Subject-wise performance
    - Utilize JavaScript libraries like Plotly.js and D3.js to create dynamic charts and graphs for enhanced visualization.
4. **Forecasting Next Semester's Results:**
    
    - Implement predictive analytics techniques to forecast students' performance in upcoming semesters based on historical data and trends.
    - Provide educators with insights into potential areas for improvement and opportunities for intervention.
5. **Student Search and Profile:**
    
    - Enable educators to search for students by roll number or name.
    - Provide a detailed profile for each student, including past semester marks, subject-wise performance, and performance trends.
    - Display a chart of the student's performance over time for quick insights.
6. **Table View and Filtering:**
    
    - Present extracted results in a tabular format on the website, allowing educators to view and analyze data easily.
    - Implement filtering options to enable educators to filter data based on criteria such as grades, total marks, or subjects.
7. **Subject-wise Reports:**
    
    - Generate detailed subject-wise reports for each semester, providing insights into student performance in individual subjects.
    - Allow educators to drill down into specific subjects and analyze performance metrics in detail.

### **Tech Stack:**

- **Frontend**: React.js for building dynamic user interfaces and interactive visualizations.
- **Backend**: FastAPI for handling API requests, data processing, and serving the frontend application.
- **Database**: PostgreSQL for storing structured student performance data and supporting complex queries.
- **Data Analysis**: Python libraries like pandas, NumPy, and scikit-learn for data manipulation, analysis, and visualization.
- **Authentication**: Implement Google OAuth 2.0 for secure authentication and access to Google APIs (Drive and Sheets).
- **Deployment**: Deploy the application on AWS (Amazon Web Services) for scalability and accessibility, utilizing services like Amazon EC2, RDS, and S3.

**Conclusion:** The Comprehensive Student Performance Dashboard offers educators a comprehensive solution for analyzing, visualizing, and forecasting student performance data. By leveraging a single-page application (SPA) architecture with React.js for the frontend and FastAPI for the backend, this dashboard provides a seamless user experience and efficient data processing capabilities. With its user-friendly interface, customizable features, and predictive analytics capabilities, the dashboard empowers educators to make data-driven decisions and support student success effectively.
