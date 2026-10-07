import os
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor

SRC = r'C:\Users\TEJESWAR\Desktop\YouTube-Data-Analysis\DAE_Reference_Document.docx'
DST = r'C:\Users\TEJESWAR\Desktop\YouTube-Data-Analysis\YouTube_Data_Analysis_System_DAE_Report.docx'

doc = Document(SRC)

def replace_para_text(p, new_text):
    if not p.runs:
        return
    if new_text == "":
        for r in p.runs:
            r.text = ""
        num_pr = p._p.xpath('./w:pPr/w:numPr')
        if num_pr:
            num_pr[0].getparent().remove(num_pr[0])
    else:
        # Keep formatting of first run, clear the rest
        p.runs[0].text = new_text
        for r in p.runs[1:]:
            r.text = ""

# Exact matches for entire paragraph strings
PARA_MAPPINGS = {
    # General / Titles
    "Employee Attendance and Salary Analysis System": "YouTube Data Analysis System",
    "EMPLOYEE ATTENDANCE AND SALARY ANALYSIS SYSTEM": "YOUTUBE DATA ANALYSIS SYSTEM",
    "Date: 21-09-2026": "Date: 29-09-2026",

    # Abstract
    "The Employee Attendance and Salary Analysis System is a data analysis project developed to analyze employee attendance, working hours, leave patterns, overtime, and salary information. Organizations generate large amounts of employee-related data, and manually analyzing this information can be time-consuming and prone to errors.": "The YouTube Data Analysis System is a data analysis project developed to analyze trending videos, channels, categories, publishing patterns, and engagement. YouTube generates large amounts of video data daily, and analyzing this manually is time-consuming and prone to errors.",
    
    "The proposed system uses data analysis techniques to clean, process, analyze, and visualize employee-related data. The system calculates important measures such as attendance percentage, absenteeism, working hours, overtime pay, deductions, and net salary. Different statistical methods and visualization techniques are used to identify meaningful patterns and relationships in the data.": "The proposed system uses data analysis techniques to clean, process, analyze, and visualize YouTube trending video data. The system calculates important measures such as engagement, engagement rate, category counts, and publishing trends. Different statistical methods and visualization techniques are used to identify meaningful patterns and relationships in the data.",
    
    "The project also performs department-wise analysis to compare attendance, salary, overtime, absenteeism, and payroll. Graphical representations such as bar charts, pie charts, histograms, box plots, line charts, and scatter plots help in understanding the data more easily.": "The project also performs category-wise and channel-wise analysis. Graphical representations such as bar charts, pie charts, histograms, box plots, line charts, and scatter plots help in understanding the data more easily.",
    
    "The system provides useful insights that can support HR departments and management in understanding employee attendance and salary patterns and making data-driven": "The system provides useful insights that can support content creators and analysts in understanding video engagement patterns and making data-driven",
    
    "decisions. The project can further be extended with predictive analytics and anomaly detection.": "decisions. The processed data is also presented via a React/Vite interactive dashboard.",

    # Chapter 1
    "Employee attendance and salary management are important activities in every organization. Attendance records provide information about employee presence, absence, leave, working hours, and overtime. Salary records contain information such as basic salary, bonuses, overtime payments, deductions, taxes, and net salary.": "YouTube is a massive video-sharing platform generating enormous amounts of daily data. Trending records provide information about a video's presence, channel, category, publishing time, and engagement. Engagement records contain information such as views, likes, and comments.",
    
    "Traditional methods of analyzing employee records generally depend on spreadsheets and manual calculations. When the amount of data increases, it becomes difficult to identify important patterns and relationships between attendance and salary.": "Traditional methods of analyzing video records generally depend on basic spreadsheets. When the amount of data increases, it becomes difficult to identify important patterns and relationships between publishing time, categories, and engagement.",
    
    "The Employee Attendance and Salary Analysis System uses data analysis techniques to convert raw employee records into useful information. Python libraries such as Pandas, NumPy, Matplotlib, and Seaborn can be used for data processing, statistical analysis, and visualization.": "The YouTube Data Analysis System uses data analysis techniques to convert raw trending records into useful information. Python libraries such as Pandas, NumPy, and Matplotlib are used for data processing, statistical analysis, and visualization.",
    
    "The project analyzes employee attendance and salary information and presents the results using meaningful graphs and statistical measures. This makes the information easier to understand and helps identify trends in attendance, salary, overtime, and departmental performance.": "The project analyzes YouTube trending video information and presents the results using meaningful graphs and a React dashboard. This makes the information easier to understand and helps identify trends in categories, engagement, and channel performance.",
    
    "Organizations maintain large amounts of employee attendance and salary information. Manual analysis of this information can require considerable time and may result in calculation errors.": "YouTube maintains large amounts of trending video information. Manual analysis of this information can require considerable time and may result in calculation errors.",
    
    # 1.2 Bullets
    "Employees with low attendance.": "Videos with low engagement.",
    "Department-wise attendance patterns.": "Category-wise trending patterns.",
    "Absenteeism trends.": "Publishing time trends.",
    "Working-hour patterns.": "Channel-wise performance patterns.",
    "Overtime patterns.": "Category-wise views distribution.",
    "Salary distribution.": "Engagement rate distribution.",
    "Department-wise payroll.": "Category-wise engagement.",
    "Relationships between attendance and salary.": "Relationships between views and likes.",
    "Relationships between overtime and salary.": "Relationships between views and comments.",
    
    "Therefore, there is a need for a data analysis system that can process employee attendance and salary information and present useful insights through statistical analysis and visualization.": "Therefore, there is a need for a data analysis system that can process YouTube trending video information and present useful insights through statistical analysis, visualization, and an interactive dashboard.",

    # 1.3 Bullets
    "To analyze employee attendance data.": "To analyze YouTube trending video data.",
    "To calculate attendance and absenteeism percentages.": "To calculate engagement and engagement rates.",
    "To analyze working hours and overtime.": "To analyze publishing years, months, days, and hours.",
    "To analyze employee salary information.": "To analyze channel and category information.",
    "To calculate deductions and net salary.": "To compare videos across different categories.",
    "To compare employees across different departments.": "To identify views and engagement trends.",
    "To identify attendance and salary trends.": "To analyze relationships between views, likes, and comments.",
    "To analyze relationships between attendance, working hours, overtime, and salary.": "To develop an interactive React/Vite dashboard.",
    "To represent the results using different visualization techniques.": "To represent the results using different visualization techniques.",
    "To provide meaningful insights that support data-driven decision-making.": "To provide meaningful insights that support content creators.",

    # 1.4
    "The scope of the project includes employee, attendance, leave, overtime, and salary analysis.": "The scope of the project includes video, channel, category, publishing time, and engagement analysis.",
    
    "Employee information analysis.": "Video information analysis.",
    "Department-wise employee analysis.": "Channel performance analysis.",
    "Attendance analysis.": "Category distribution analysis.",
    "Absenteeism analysis.": "Video views analysis.",
    "Leave analysis.": "Video likes analysis.",
    "Working-hour analysis.": "Video comments analysis.",
    "Overtime analysis.": "Engagement analysis.",
    "Salary analysis.": "Publishing-time analysis.",
    "Payroll analysis.": "Statistical analysis.",
    "Statistical analysis.": "Data visualization.",
    "Data visualization.": "Interactive dashboard presentation.",
    "Department comparison.": "Insight generation.",
    "Relationship analysis.": "",
    
    "The system can also be extended in the future to include predictive analytics, anomaly detection, automated reporting, and real-time attendance integration.": "The system can also be extended in the future to include predictive analytics, real-time YouTube API integration, and automated reporting.",

    # Chapter 2
    "The dataset used for the project contains employee-related information required for attendance and salary analysis.": "The dataset used for the project contains video-related information required for trending and engagement analysis.",
    "The project dataset is organized around employee, attendance, leave, overtime, and salary information. These data categories provide the required information for performing employee attendance and salary analysis.": "The project dataset is organized around video, channel, category, publish time, and engagement information. These data categories provide the required information for performing video engagement analysis.",
    "The project specification identifies employee ID, employee name, gender, department, designation, joining date, salary, attendance status, working time, leave information, overtime, and salary components as important attributes.": "The project specification identifies video_id, trending_date, title, channel_title, category_id, publish_time, views, likes, dislikes, and comment_count as important attributes.",
    "The dataset is designed to represent employee attendance and salary information.": "The dataset is designed to represent YouTube trending video information.",
    
    # 2.2 Bullets
    "Employee Information": "Video Information",
    "Contains basic information about employees such as:": "Contains basic information about videos such as:",
    "Employee ID": "video_id",
    "Employee Name": "trending_date",
    "Gender": "title",
    "Department": "channel_title",
    "Designation": "category_id",
    "Joining Date": "publish_time",
    "Basic Salary": "",
    
    "Attendance Information": "Interaction Metrics",
    "Contains employee attendance information such as:": "Contains video interaction information such as:",
    "Attendance ID": "views",
    "Date": "likes",
    "Check-In Time": "dislikes",
    "Check-Out Time": "comment_count",
    "Attendance Status": "",
    
    "Leave Information": "Derived Features",
    "Leave ID": "publish_year",
    "Leave Date": "publish_month",
    "Leave Type": "publish_day",
    "Reason": "publish_hour",
    "Approval Status": "engagement",
    "Overtime Information": "engagement_rate",
    "Overtime ID": "",
    "Overtime Hours": "",
    "Hourly Rate": "",
    "Overtime Amount": "",
    "Salary Information": "",
    "Salary ID": "",
    "Month": "",
    "Overtime Pay": "",
    "Bonus": "",
    "Leave Deduction": "",
    "Tax": "",
    "Other Deduction": "",
    "Net Salary": "",

    # Chapter 3
    "df = pd.read_csv(\"employee_attendance_salary.csv\")": "df = pd.read_csv(\"INvideos.csv\")",
    "For example, salary values and working hours may have very different numerical ranges.": "For example, views and comments may have very different numerical ranges.",
    "Present → 1": "True → 1",
    "Absent → 0": "False → 0",
    "For example, if the Department column contains:": "For example, if the Category column contains:",
    "HR": "Music",
    "IT": "Entertainment",
    "Finance": "Education",
    "Sales": "Gaming",
    "df_encoded = pd.get_dummies(df, columns=['Department'])": "df_encoded = pd.get_dummies(df, columns=['category_id'])",
    
    "Converting check-in and check-out values into time format.": "Converting dates into proper date format.",
    "Calculating working hours.": "Extracting publish year, month, and day.",
    "Calculating attendance percentage.": "Extracting publish hour.",
    "Calculating absenteeism percentage.": "Calculating engagement.",
    "Calculating overtime pay.": "Calculating engagement rate.",
    "Calculating total deductions.": "",
    "Calculating net salary.": "",
    "Standardizing department and designation names.": "",
    
    "The project methodology specifically identifies working hours, attendance percentage, absence percentage, overtime pay, total deductions, and net salary as useful transformed fields.": "The project methodology specifically identifies publish year, month, day, hour, engagement, and engagement rate as useful transformed fields.",

    # Chapter 4 Flow/Methodology
    "Data Collection → Data Cleaning → Data Processing → Data Analysis → Visualization → Dashboard → Insights": "Data Loading → Data Exploration → Data Cleaning → Date/Time Conversion → Feature Engineering → EDA → Visualization → Dashboard → Insights",
    "Data Collection": "Data Loading",
    "Data Storage": "Data Exploration",
    "Data Cleaning": "Data Cleaning",
    "Data Transformation": "Date/Time Conversion",
    "Exploratory Data Analysis": "Feature Engineering",
    "Statistical Analysis": "Exploratory Data Analysis",
    "Data Visualization": "Statistical Analysis",
    "Dashboard Development": "Data Visualization",
    "Insight Generation": "Dashboard Development",
    "This workflow follows the methodology defined for the project.": "Insight Generation",
    
    "Collect Employee Data": "Load INvideos.csv",
    "Collect Attendance Data": "Dataset Exploration",
    "Collect Salary Data": "Missing Value Check",
    "Store Data": "Duplicate / Invalid ID Check",
    "Data Preprocessing": "Date / Time Conversion",
    "Export Processed Data": "Export youtube_dashboard_data.csv",
    "Dashboard": "React/Vite Dashboard",

    # Chapter 5 EDA
    "Employee Analysis": "Video Analysis",
    "Number of employees.": "Number of videos.",
    "Employees by department.": "Videos by category.",
    "Employees by designation.": "Videos by channel.",
    "Average salary.": "Average views.",
    "Minimum salary.": "Minimum views.",
    "Maximum salary.": "Maximum views.",
    "Attendance Analysis": "Engagement Analysis",
    "Present days.": "Total likes.",
    "Absent days.": "Total dislikes.",
    "Leave days.": "Total comments.",
    "Attendance percentage.": "Average engagement rate.",
    "Absenteeism percentage.": "",
    "Average working hours.": "",
    "Salary Analysis": "Publishing Analysis",
    "Basic salary.": "Publishing year trends.",
    "Bonus.": "Publishing day trends.",
    "Deductions.": "Publishing hour trends.",
    "Net salary.": "",
    "Total payroll.": "",
    "Department Analysis": "Category Analysis",
    "Departments are compared using:": "Categories are compared using:",
    "Average attendance.": "Average views.",
    "Average salary.": "Average likes.",
    "Total payroll.": "Average comments.",
    "Absenteeism.": "Average engagement.",
    "Overtime hours.": "",
    "print(df['Basic_Salary'].mean())": "print(df['views'].mean())",
    "print(df['Basic_Salary'].median())": "print(df['views'].median())",
    "print(df['Basic_Salary'].std())": "print(df['views'].std())",
    "df.groupby('Department')['Basic_Salary'].mean()": "df.groupby('category_id')['views'].mean()",
    "It calculates the average salary for each department.": "It calculates the average views for each category.",

    # Chapter 6 & 9 MAPPINGS
    '6.1 Bar Graph': '6.1 Bar Chart',
    'For example, department-wise employee count can be visualized using:': 'Top 10 Channels by Trending Videos.',
    'df[\'Department\'].value_counts().plot(kind=\'bar\')': 'Top Videos by Views.',
    'plt.title(\'Employees by Department\')': '6.3 Category Visualization',
    'plt.xlabel(\'Department\')': 'Category Counts.',
    'plt.ylabel(\'Number of Employees\')': '6.4 Category Visualization',
    'The bar graph helps compare the number of employees in different departments.': 'Category-wise Views.',
    
    '6.2 Pie Chart': '6.5 Publishing Analysis',
    'A pie chart can be used to represent the proportion of attendance statuses.': 'Videos by Month.',
    'df[\'Status\'].value_counts().plot(': '6.6 Publishing Analysis',
    'kind=\'pie\',': 'Videos by Day.',
    'autopct=\'%1.1f%%\',': '6.7 Publishing Analysis',
    ')': 'Videos by Hour.',
    'plt.title(\'Attendance Status Distribution\')': '6.8 Scatter Plot',
    'plt.ylabel(\'\')': 'Views vs Likes.',
    'The chart provides a visual representation of the proportion of different attendance statuses.': '6.9 Scatter Plot',
    
    '6.3 Histogram': 'Views vs Comments.',
    'A histogram is used to understand the distribution of numerical values such as salary.': '6.10 Project-Specific Dashboard Visualizations',
    'plt.hist(df[\'Basic_Salary\'], bins=10)': 'Overview Dashboard',
    'plt.title(\'Basic Salary Distribution\')': 'Trending Videos',
    'plt.xlabel(\'Basic Salary\')': 'Channels',
    'plt.ylabel(\'Frequency\')': 'Engagement',
    'The histogram shows how salary values are distributed.': 'Publishing Insights',
    
    # Clear the rest of Chapter 6
    '6.4 Box Plot': '',
    'A box plot is useful for understanding salary distribution and identifying possible outliers.': '',
    'sns.boxplot(x=df[\'Basic_Salary\'])': '',
    'plt.title(\'Basic Salary Box Plot\')': '',
    'The box plot displays the median, quartiles, spread, and possible outliers.': '',
    '6.5 Line Chart': '',
    'A line chart can be used to display monthly attendance or salary trends.': '',
    'monthly_salary = df.groupby(\'Month\')[\'Net_Salary\'].mean()': '',
    'monthly_salary.plot(kind=\'line\', marker=\'o\')': '',
    'plt.title(\'Monthly Average Net Salary\')': '',
    'plt.xlabel(\'Month\')': '',
    'plt.ylabel(\'Average Net Salary\')': '',
    'The line chart helps identify changes or trends over time.': '',
    '6.6 Scatter Plot': '',
    'A scatter plot can be used to analyze the relationship between two numerical variables.': '',
    'plt.scatter(df[\'Overtime_Hours\'], df[\'Net_Salary\'])': '',
    'plt.title(\'Overtime Hours vs Net Salary\')': '',
    'plt.xlabel(\'Overtime Hours\')': '',
    'plt.ylabel(\'Net Salary\')': '',
    'This visualization helps examine whether overtime hours are associated with changes in net salary.': '',
    '6.7 Project-Specific Visualizations': '',
    'The project-specific visualizations include:': '',
    'Department-wise employee count.': '',
    'Attendance status distribution.': '',
    'Salary distribution.': '',
    'Department-wise average salary.': '',
    'Department-wise attendance.': '',
    'Monthly attendance trend.': '',
    'Overtime hours analysis.': '',
    'Overtime versus salary.': '',
    'Working hours versus salary.': '',
    'Absenteeism versus salary.': '',
    'The project specifically identifies attendance vs salary, overtime vs salary, working hours vs salary, and absenteeism vs salary as relationships for analysis.': '',
    
    # Chapter 7
    'Employee distribution.': 'Total records: 33,089 cleaned records.',
    'Department-wise employee count.': 'Total views: Approximately 32.97 billion.',
    'Attendance distribution.': 'Total likes: Approximately 846.67 million.',
    'Absenteeism.': 'Average engagement rate: Approximately 2.45%.',
    'Working hours.': 'Average views: Approximately 996,342.',
    'Overtime.': 'Average likes: Approximately 25,387.',
    'Salary distribution.': 'Average comments: Approximately 2,525.',
    'Department-wise salary.': 'Channel-level analysis.',
    'Total payroll.': 'Category-level analysis.',
    'Relationship between attendance and salary.': 'Publishing patterns.',
    'Relationship between overtime and salary.': 'Engagement analysis.',
    
    'Department-wise employee counts show how employees are distributed across departments.': 'Category counts show how videos are distributed across categories.',
    'Attendance analysis shows the distribution of present, absent, and leave records.': 'Publishing analysis shows the distribution of videos by month, day, and hour.',
    'Salary analysis shows salary distribution among employees.': 'Engagement analysis shows engagement rate distribution.',
    'Overtime analysis shows additional working hours and overtime payments.': 'Views analysis shows the total views across channels.',
    'Department analysis allows comparison of salary and attendance patterns.': 'Category analysis allows comparison of views and engagement patterns.',
    
    'The project demonstrates how data analysis techniques can be applied to employee attendance and salary information.': 'The project demonstrates how data analysis techniques can be applied to YouTube trending video information.',
    'The results can help HR personnel understand employee attendance patterns, salary distribution, overtime, absenteeism, and departmental payroll.': 'The results can help content creators understand video publishing patterns, engagement rates, and category performance.',

    # Chapter 8
    'Figure 8.8: Employees by Department – Bar Chart.': 'Figure 8.8: Overview Dashboard.',
    'Figure 8.9: Attendance Status – Pie Chart.': 'Figure 8.9: Trending Videos.',
    'Figure 8.10: Salary Distribution – Histogram.': 'Figure 8.10: Channels.',
    'Figure 8.11: Salary Distribution – Box Plot.': 'Figure 8.11: Engagement.',
    'Figure 8.12: Monthly Salary/Attendance Trend – Line Chart.': 'Figure 8.12: Publishing Insights.',
    'Figure 8.13: Overtime Hours vs Net Salary – Scatter Plot.': '',
    'Figure 8.14: Department-wise Salary Analysis.': '',
    'Figure 8.15: Department-wise Attendance Analysis.': '',
    'Analysis Output: Department-wise attendance, salary, overtime, absenteeism, and payroll results.': 'Analysis Output: Category-wise views, likes, comments, and engagement results.',

    # Chapter 9
    'The Employee Attendance and Salary Analysis System provides an effective approach for analyzing employee attendance and salary information.': 'The project analyzes the India YouTube Trending Videos dataset using Python, Pandas and exploratory data analysis techniques.',
    'The project uses data preprocessing, exploratory data analysis, statistical techniques, and visualization to transform raw employee records into meaningful information.': 'The data was cleaned and processed to study views, likes, comments, channels, categories, publishing patterns and engagement.',
    'The system analyzes employee attendance, absenteeism, working hours, leave, overtime, salary, deductions, and net salary. Department-wise analysis helps compare employee distribution, attendance, salary, overtime, and payroll.': 'The processed dataset was exported as youtube_dashboard_data.csv and used in the React/Vite dashboard.',
    'Different visualization techniques such as bar charts, pie charts, histograms, box plots, line charts, and scatter plots make the analysis easier to understand.': 'The dashboard presents the analysis through interactive visualizations and helps users understand patterns within the dataset.',
    'Overall, the project demonstrates how data analysis can be used to identify patterns and relationships in employee-related data and support data-driven decision-making.': '',
    
    'Incorrect or missing attendance records may affect the results.': 'The dataset represents historical trending videos and does not contain every YouTube video.',
    'The current project mainly focuses on historical data analysis.': 'The results depend on the attributes available in the dataset.',
    'Real-time attendance integration is not included.': 'Real-time YouTube data integration is not part of the current implementation.',
    'Predictive analysis is optional and is not part of the core implementation.': 'The project does not predict future video performance.',
    'The accuracy of insights depends on the available attributes and data records.': 'Engagement analysis is limited to the available likes and comment data.',
    'External factors affecting employee attendance and salary are not directly represented in the dataset.': 'External factors affecting video popularity are not fully represented.',
    
    'Machine-learning-based attendance prediction.': 'Real-time YouTube API integration.',
    'Salary forecasting.': 'Automated dataset updates.',
    'Absenteeism prediction.': 'Trend forecasting.',
    'Anomaly detection.': 'Predictive analytics for video performance.',
    'Automated report generation.': 'Sentiment analysis if comment text is available.',
    'Real-time attendance integration.': 'Automated report generation.',
    'Advanced Power BI dashboards.': 'Advanced dashboard filtering.',
    'Automated payroll analysis.': 'More detailed category and channel analysis.',
    'Employee-level performance analysis.': '',
    'Integration with organizational HR systems.': '',
    'The project specification also identifies prediction, salary forecasting, anomaly detection, automated reports, and real-time attendance integration as possible future enhancements.': '',
    
    'Project Dataset – Employee Attendance and Salary Dataset.': 'YouTube Trending Videos Dataset / INvideos.csv.',
    'Employee Attendance and Salary Analysis System – Project Specification Document.': 'YouTube Data Analysis System – Project Documentation.',
    'Microsoft Power BI Documentation – Data Visualization and Business Intelligence.': 'React and Vite Documentation.',
    'Seaborn Documentation – Statistical Data Visualization.': 'PapaParse Documentation.',
}

TABLE_REPLACEMENTS = {
    "A  ABHIRAM VARMA": "TEJESWAR DOOLLA",
    "G SRINIVAS": "SYED SAIF HUSSAIN",
    "P NEELIMA": "LOKESH KAPPARATI",
    "T YAMINI": "GANUSAI VECHALAPU",
    "ABHIRAM VARMA": "TEJESWAR DOOLLA",
    "P NEEELIMA": "LOKESH KAPPARATI",
    "(25B11AI076)": "(25B11AIB79)",
    "(25B11AI349)": "(25B11AIB59)",
    "(25B11AI976)": "(25B11AI495)",
    "(25B11AIB61)": "(25B11AIC55)",
    
    "Employee ID": "video_id",
    "Employee Name": "trending_date",
    "Gender": "title",
    "Department": "channel_title",
    "Designation": "category_id",
    "Joining Date": "publish_time",
    "Salary": "views",
    "Attendance Status": "likes",
    "Working Time": "dislikes",
    "Leave Information": "comment_count",
    "Overtime": "publish_year",
    "Salary Components": "publish_month",
    
    "Unique identifier for each employee": "Unique identifier for each YouTube video",
    "Full name of the employee": "Date when the video appeared on the trending page",
    "Gender of the employee": "Title of the YouTube video",
    "Department where the employee works": "Name of the YouTube channel",
    "Job designation or role": "Numeric category ID",
    "Date when the employee joined": "Date and time when the video was published",
    "Monthly basic salary": "Total view count",
    "Whether the employee is present or absent": "Total number of likes",
    "Total hours worked by the employee": "Total number of dislikes",
    "Leave requested or taken by employee": "Total number of comments",
    "Additional overtime hours worked": "Derived publish year",
    "Allowances, bonuses, deductions, taxes, net salary": "Derived publish month",
}

for p in doc.paragraphs:
    text = p.text.strip()
    if text in PARA_MAPPINGS:
        replace_para_text(p, PARA_MAPPINGS[text])

for t in doc.tables:
    for r in t.rows:
        for c in r.cells:
            for p in c.paragraphs:
                text = p.text.strip()
                if text in TABLE_REPLACEMENTS:
                    replace_para_text(p, TABLE_REPLACEMENTS[text])
                elif text in PARA_MAPPINGS:
                    replace_para_text(p, PARA_MAPPINGS[text])

# Handle ASCII flowchart -> Table conversion exactly as we did before, but safely
def insert_single_col_table(ref_para, items):
    table = doc.add_table(rows=len(items), cols=1)
    table.style = 'Table Grid'
    for i, item in enumerate(items):
        cell = table.cell(i, 0)
        cell.text = item
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(11)
    ref_para._p.addnext(table._tbl)

arch_lines = [
    "INvideos.csv", "Python / Google Colab", "Pandas Data Processing", 
    "Data Cleaning", "Date / Time Conversion", "Feature Engineering", "Exploratory Data Analysis", 
    "Statistical Analysis", "Data Visualization", "youtube_dashboard_data.csv", 
    "React / Vite Dashboard", "Insights"
]
flow_lines = [
    "START", "Load INvideos.csv", "Dataset Exploration", "Missing Value Check",
    "Duplicate / Invalid ID Check", "Data Cleaning", "Date / Time Conversion",
    "Feature Engineering", "Exploratory Data Analysis", "Statistical Analysis",
    "Data Visualization", "Export youtube_dashboard_data.csv", "React/Vite Dashboard",
    "Generate Insights", "Generate Final Report", "END"
]

arch_found = False
flow_found = False
for p in doc.paragraphs:
    if p.text.strip() == "4.2 System Workflow / Architecture":
        arch_found = True
    elif arch_found and p.text.strip() == "The system architecture can be represented as:":
        arch_items = []
        for x in arch_lines:
            arch_items.append(x)
            if x != arch_lines[-1]: arch_items.append("↓")
        insert_single_col_table(p, arch_items)
        arch_found = False
    elif p.text.strip() == "4.3 Flowchart":
        flow_found = True
    elif flow_found and p.text.strip() == "The flowchart is as follows:":
        flow_items = []
        for x in flow_lines:
            flow_items.append(x)
            if x != flow_lines[-1]: flow_items.append("↓")
        insert_single_col_table(p, flow_items)
        flow_found = False

ascii_lines = [
    "Employee Data", "Attendance Data", "Leave Data", "Overtime Data", "Salary Data",
    "|", "v", "+----------------------+", "|    Data Processing   |",
    "|    Data Cleaning     |", "| Feature Engineering  |", "| Exploratory Analysis |",
    "| Statistical Analysis |", "| Data Visualization   |", "| Dashboard / Reports  |",
    "START", "Load Employee Dataset", "Load Attendance Dataset", "Load Leave Dataset",
    "Load Overtime Dataset", "Load Salary Dataset", "Dataset Exploration",
    "Missing Value Check", "Duplicate Value Check", "Data Cleaning",
    "Date / Time Conversion", "Feature Engineering", "Exploratory Data Analysis",
    "Statistical Analysis", "Data Visualization", "Export Processed Data",
    "Dashboard Development", "Generate Insights", "Generate Final Report", "END", "Insights"
]

for p in doc.paragraphs:
    t = p.text.strip()
    if t in ascii_lines or t == "v" or t == "|" or "+----" in t or "| " in t:
        replace_para_text(p, "")

doc.save(DST)
print(f"SUCCESS: Saved PERFECT report to {DST}")
