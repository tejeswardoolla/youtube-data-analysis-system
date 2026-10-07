import re
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor

SRC = r'C:\Users\TEJESWAR\Desktop\YouTube-Data-Analysis\DAE_Reference_Document.docx'
DST = r'C:\Users\TEJESWAR\Desktop\YouTube-Data-Analysis\YouTube_Data_Analysis_System_DAE_Report_Final_Fixed.docx'

doc = Document(SRC)

def replace_text_preserve_runs(old_text, new_text):
    # Process paragraphs
    for p in doc.paragraphs:
        if old_text in p.text:
            replaced = False
            for r in p.runs:
                if old_text in r.text:
                    r.text = r.text.replace(old_text, new_text)
                    replaced = True
            if not replaced:
                if p.text.strip() == old_text.strip():
                    if p.runs:
                        p.runs[0].text = p.runs[0].text.replace(old_text.strip(), new_text)
                        for r in p.runs[1:]: r.text = ""
                else:
                    if p.runs:
                        full_new = p.text.replace(old_text, new_text)
                        p.runs[0].text = full_new
                        for r in p.runs[1:]: r.text = ""
    # Process tables
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    if old_text in p.text:
                        replaced = False
                        for run in p.runs:
                            if old_text in run.text:
                                run.text = run.text.replace(old_text, new_text)
                                replaced = True
                        if not replaced:
                            if p.text.strip() == old_text.strip():
                                if p.runs:
                                    p.runs[0].text = p.runs[0].text.replace(old_text.strip(), new_text)
                                    for run in p.runs[1:]: run.text = ""
                            else:
                                if p.runs:
                                    full_new = p.text.replace(old_text, new_text)
                                    p.runs[0].text = full_new
                                    for run in p.runs[1:]: run.text = ""

# 1. Global replacements for text that shouldn't change formatting
REPLACEMENTS = [
    ("Employee Attendance and Salary Analysis System", "YouTube Data Analysis System"),
    ("EMPLOYEE ATTENDANCE AND SALARY ANALYSIS SYSTEM", "YOUTUBE DATA ANALYSIS SYSTEM"),
    ("employee_attendance_salary.csv", "INvideos.csv"),
    ("Employee attendance and salary management are important activities", "YouTube is a massive video-sharing platform, generating enormous amounts of daily data."),
    ("Employee attendance and salary management", "YouTube trending video analysis"),
    ("Employee attendance", "YouTube trending data"),
    ("attendance and salary", "video engagement"),
    ("Attendance and salary", "Video engagement"),
    ("Attendance and Salary", "Video Engagement"),
    ("attendance", "engagement"),
    ("salary", "popularity"),
    ("employee records", "video records"),
    ("employees", "videos"),
    ("HR departments", "content creators"),
    ("HR personnel", "data analysts"),
    ("department-wise", "category-wise"),
    ("Department-wise", "Category-wise"),
    ("21-09-2026", "29-09-2026"),
]

for old, new in REPLACEMENTS:
    replace_text_preserve_runs(old, new)

# 2. Fix the Certificate Names in Table 0
replace_text_preserve_runs("A  ABHIRAM VARMA", "TEJESWAR DOOLLA")
replace_text_preserve_runs("G SRINIVAS", "SYED SAIF HUSSAIN")
replace_text_preserve_runs("P NEELIMA", "LOKESH KAPPARATI")
replace_text_preserve_runs("T YAMINI", "GANUSAI VECHALAPU")

replace_text_preserve_runs("ABHIRAM VARMA", "TEJESWAR DOOLLA")
replace_text_preserve_runs("P NEEELIMA", "LOKESH KAPPARATI") # Template typo

replace_text_preserve_runs("25B11AI076", "25B11AIB79")
replace_text_preserve_runs("25B11AI349", "25B11AIB59")
replace_text_preserve_runs("25B11AI976", "25B11AI495")
replace_text_preserve_runs("25B11AIB61", "25B11AIC55")

# 3. Chapter 2 Empty Bullets / Content Fix
ch2_mappings = [
    ("Employee Information", "Video Information"),
    ("Employee ID", "video_id"),
    ("Employee Name", "trending_date"),
    ("Gender", "title"),
    ("Department", "channel_title"),
    ("Designation", "category_id"),
    ("Joining Date", "publish_time"),
    ("Basic Salary", "views"),
    ("Attendance Information", "Interaction Metrics"),
    ("Attendance ID", "likes"),
    ("Date", "dislikes"),
    ("Check-In Time", "comment_count"),
    ("Check-Out Time", "publish_year"),
    ("Attendance Status", "publish_month"),
    ("Leave Information", "Derived Features"),
    ("Leave ID", "publish_day"),
    ("Leave Date", "publish_hour"),
    ("Leave Type", "engagement"),
    ("Reason", "engagement_rate"),
]

for old, new in ch2_mappings:
    replace_text_preserve_runs(old, new)

# Now delete the remaining empty bullets in Chapter 2 without losing page breaks
# Basically, anything after "Reason" in the original list up to the next section
words_to_clear = [
    "Approval Status",
    "Overtime Information",
    "Overtime ID",
    "Overtime Hours",
    "Hourly Rate",
    "Overtime Amount",
    "Salary Information",
    "Salary ID",
    "Month",
    "Overtime Pay",
    "Bonus",
    "Leave Deduction",
    "Tax",
    "Other Deduction",
    "Net Salary"
]

for p in doc.paragraphs:
    if p.text.strip() in words_to_clear:
        # Clear the text
        for r in p.runs: r.text = ""
        # Remove bullet property (w:numPr) so it's not an empty bullet
        num_pr = p._p.xpath('./w:pPr/w:numPr')
        if num_pr:
            num_pr[0].getparent().remove(num_pr[0])

# Do the same for Chapter 1.4 Scope bullets
scope_replacements = [
    ("Employee information analysis.", "YouTube trending video analysis."),
    ("Department-wise employee analysis.", "Channel performance analysis."),
    ("Attendance analysis.", "Category distribution analysis."),
    ("Absenteeism analysis.", "Video views analysis."),
    ("Leave analysis.", "Video likes analysis."),
    ("Working-hour analysis.", "Video comment analysis."),
    ("Overtime analysis.", "Engagement analysis."),
    ("Salary analysis.", "Publishing-time analysis."),
    ("Payroll analysis.", "Statistical analysis."),
    ("Statistical analysis.", "Data visualization."),
    ("Data visualization.", "Interactive dashboard presentation."),
    ("Department comparison.", "Insight generation."),
]
for old, new in scope_replacements:
    replace_text_preserve_runs(old, new)

scope_clears = ["Relationship analysis."]
for p in doc.paragraphs:
    if p.text.strip() in scope_clears:
        for r in p.runs: r.text = ""
        num_pr = p._p.xpath('./w:pPr/w:numPr')
        if num_pr:
            num_pr[0].getparent().remove(num_pr[0])

# 4. Chapter 4 - Architecture & Flowchart (ASCII replacement)
# Instead of text, insert a table and clear the ASCII.
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
    "Data Cleaning", "Feature Engineering", "Exploratory Data Analysis", 
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

# Locate System Workflow / Architecture
arch_found = False
flow_found = False
for p in doc.paragraphs:
    if p.text.strip() == "4.2 System Workflow / Architecture":
        arch_found = True
    elif arch_found and p.text.strip() == "The system architecture can be represented as:":
        # Insert table after this paragraph
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

# Clear all the ASCII art lines
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
        # Check if it's in the actual text (not the tables we just made)
        # Actually tables are separate from doc.paragraphs in python-docx
        for r in p.runs: r.text = ""
        # Remove empty bullets if any
        num_pr = p._p.xpath('./w:pPr/w:numPr')
        if num_pr:
            num_pr[0].getparent().remove(num_pr[0])

# 5. Fix tools table (Table 2 or whichever contains Python/Power BI)
for t in doc.tables:
    if len(t.rows) > 0 and len(t.columns) == 2:
        try:
            cell_text = t.rows[0].cells[0].text
            if 'Python' in cell_text or 'Tool' in cell_text or 'Technology' in cell_text or 'Language' in cell_text:
                # This is the tools table
                pass
        except:
            pass

# 6. Global replace for any remaining "Employee" or "Salary"
replace_text_preserve_runs("Power BI", "React / Vite")
replace_text_preserve_runs("Seaborn", "Matplotlib")
replace_text_preserve_runs("seaborn as sns", "matplotlib.pyplot as plt")

doc.save(DST)
print(f"SUCCESS: Saved PERFECT report to {DST}")
