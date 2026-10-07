"""
YouTube Data Analysis System – DAE Project Report Generator
Builds YouTube_Data_Analysis_System_DAE_Report.docx from the reference template.
"""

import copy
import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import docx.opc.constants

SRC = r'C:\Users\TEJESWAR\Desktop\YouTube-Data-Analysis\DAE_Reference_Document.docx'
DST = r'C:\Users\TEJESWAR\Desktop\YouTube-Data-Analysis\YouTube_Data_Analysis_System_DAE_Report.docx'

doc = Document(SRC)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────


def update_para(para, text):
    if not para.runs:
        para.add_run(text)
        return
    para.runs[0].text = text
    for r in para.runs[1:]:
        r.text = ''

def clear_para(para):
    """Remove all text runs from a paragraph without deleting it."""
    for run in para.runs:
        run.text = ''

def set_para_text(para, text, bold=None, italic=None, font_size=None,
                  alignment=None, color=None):
    """Replace paragraph text, inheriting existing run formatting."""
    clear_para(para)
    if alignment is not None:
        para.alignment = alignment
    run = para.add_run(text)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if font_size is not None:
        run.font.size = Pt(font_size)
    if color is not None:
        run.font.color.rgb = RGBColor(*color)

def para_text(para):
    return para.text.strip()

def find_para_index(doc, needle, partial=True):
    """Return index of first paragraph whose text contains needle."""
    for i, p in enumerate(doc.paragraphs):
        if partial:
            if needle.lower() in p.text.lower():
                return i
        else:
            if p.text.strip() == needle:
                return i
    return -1

def replace_text_in_para(para, old, new):
    """Replace occurrences of old with new across all runs in para, preserving formatting."""
    for run in para.runs:
        if old.lower() in run.text.lower():
            run.text = re.sub(re.escape(old), new, run.text, flags=re.IGNORECASE)

def global_replace(doc, replacements):
    """Apply a list of (old, new) substitutions to every paragraph in the document."""
    for para in doc.paragraphs:
        for old, new in replacements:
            if old.lower() in para.text.lower():
                replace_text_in_para(para, old, new)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for old, new in replacements:
                        if old.lower() in para.text.lower():
                            replace_text_in_para(para, old, new)

def delete_paragraph(para):
    """Remove a paragraph element from the document."""
    p = para._element
    p.getparent().remove(p)

def add_run_with_fmt(para, text, bold=False, mono=False, font_size=None):
    run = para.add_run(text)
    run.bold = bold
    if mono:
        run.font.name = 'Courier New'
    if font_size:
        run.font.size = Pt(font_size)
    return run

def insert_paragraph_after(ref_para, text='', style='Normal'):
    """Insert a new paragraph directly after ref_para and return it."""
    new_p = OxmlElement('w:p')
    ref_para._element.addnext(new_p)
    new_para = doc.paragraphs[doc.paragraphs.index(ref_para) + 1]
    # In python-docx, inserted element isn't automatically wrapped;
    # simpler: use add_paragraph via rebuild approach
    # Use the reliable method:
    return new_para

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 – Global text replacements (run-level, preserves formatting)
# ─────────────────────────────────────────────────────────────────────────────

REPLACEMENTS = [
    # Title / project name
    ("Employee Attendance and Salary Analysis System", "YouTube Data Analysis System"),
    ("EMPLOYEE ATTENDANCE AND SALARY ANALYSIS SYSTEM", "YOUTUBE DATA ANALYSIS SYSTEM"),
    ("employee attendance and salary analysis system", "YouTube Data Analysis System"),
    # Student names → our team (Table 0 cells handled separately)
    ("A  ABHIRAM VARMA", "Tejeswar Doolla"),
    ("G SRINIVAS", "Syed Saif Hussain"),
    ("(25B11AI076)", "(25B11AIB79)"),
    ("(25B11AI349)", "(25B11AIB59)"),
    # Date and place
    ("21-09-2026", "29-09-2026"),
    # Dataset
    ("employee_attendance_salary.csv", "INvideos.csv"),
    ("employee attendance and salary", "YouTube trending video"),
    ("employee attendance", "YouTube trending data"),
    ("Employee Attendance", "YouTube Trending Data"),
    ("attendance and salary", "YouTube video analytics"),
    ("Attendance and Salary", "YouTube Video Analytics"),
    # Misc project-specific terms
    ("salary analysis", "video engagement analysis"),
    ("Salary Analysis", "Video Engagement Analysis"),
    ("payroll analysis", "channel performance analysis"),
    ("Payroll Analysis", "Channel Performance Analysis"),
    ("absenteeism", "low-engagement patterns"),
    ("Absenteeism", "Low-Engagement Patterns"),
    ("overtime", "comment activity"),
    ("Overtime", "Comment Activity"),
    ("net salary", "engagement rate"),
    ("Net Salary", "Engagement Rate"),
    ("basic salary", "view count"),
    ("Basic Salary", "View Count"),
    ("Power BI", "React/Vite Dashboard"),
    ("Seaborn", "Matplotlib"),
    ("seaborn as sns", "matplotlib.pyplot as plt"),
    ("import seaborn as sns", "# Matplotlib already imported above"),
    ("sns.", "plt."),
    ("employee-related", "YouTube-trending-related"),
    ("HR departments", "content analysts"),
    ("HR personnel", "data analysts"),
    ("organizational HR systems", "YouTube Analytics API"),
]

global_replace(doc, REPLACEMENTS)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 – Certificate section (paragraphs 0-23 approx)
# ─────────────────────────────────────────────────────────────────────────────

# Find and rewrite Certificate paragraph
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if 'certify that the Cornerstone project work' in t:
        clear_para(p)
        run = p.add_run(
            'This is to certify that the Cornerstone project work entitled '
            '\u201cYouTube Data Analysis System\u201d is submitted by the following students:'
        )
        break

# Rewrite guide/HOD line  – keep existing format, just make sure names correct
for p in doc.paragraphs:
    t = p.text.strip()
    if 'Chikkireddi Ramya' in t and 'Naga' in t and 'Bhargavi' in t:
        # Already correct names – just ensure titles are right
        pass  # names retained from template

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 – Fix student table (Table 0) – 4 members
# ─────────────────────────────────────────────────────────────────────────────

STUDENTS = [
    ("TEJESWAR DOOLLA",    "(25B11AIB79)"),
    ("SYED SAIF HUSSAIN",  "(25B11AIB59)"),
    ("LOKESH KAPPARATI",   "(25B11AI495)"),
    ("GANUSAI VECHALAPU",  "(25B11AIC55)"),
]

table0 = doc.tables[0]
while len(table0.rows) < 4:
    table0.add_row()

for row_idx, (name, sid) in enumerate(STUDENTS):
    row = table0.rows[row_idx]
    # Cell 0: name
    p0 = row.cells[0].paragraphs[0]
    clear_para(p0)
    rn0 = p0.add_run(name)
    rn0.bold = True
    # Cell 1: ID
    p1 = row.cells[1].paragraphs[0]
    clear_para(p1)
    rn1 = p1.add_run(sid)
    rn1.bold = True

# Update Table 1 on Page 2 (Declaration signature block)
table1 = doc.tables[1]
STUDENTS_TABLE1 = [
    ("              TEJESWAR DOOLLA                ", "(25B11AIB79)   "),
    ("             SYED SAIF HUSSAIN",               "(25B11AIB59) "),
    ("             LOKESH KAPPARATI",                "(25B11AI495) "),
    ("             GANUSAI VECHALAPU",               "(25B11AIC55)"),
]
for idx, (name, roll) in enumerate(STUDENTS_TABLE1):
    row_idx = 2 + idx
    if row_idx < len(table1.rows):
        row = table1.rows[row_idx]
        p0 = row.cells[0].paragraphs[0]
        clear_para(p0)
        rn0 = p0.add_run(name)
        rn0.bold = True
        p1 = row.cells[1].paragraphs[0]
        clear_para(p1)
        rn1 = p1.add_run(roll)
        rn1.bold = True

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 – Declaration section
# ─────────────────────────────────────────────────────────────────────────────

for p in doc.paragraphs[20:40]:
    t = p.text.strip()
    if t.startswith('We hereby declare that the project entitled'):
        update_para(p, 
            'We hereby declare that the project entitled \u201cYOUTUBE DATA ANALYSIS SYSTEM\u201d '
            'is our original work and is submitted to ADITYA UNIVERSITY, Surampalem, in partial '
            'fulfillment of the requirements for the award of the B.Tech. degree in Artificial '
            'Intelligence and Machine learning-'
        )
    if 'Place:Surampalem' in t or 'Place: Surampalem' in t:
        update_para(p, 'Place:Surampalem\nDate: 29-09-2026')

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 – Abstract
# ─────────────────────────────────────────────────────────────────────────────

abstract_paras = []
in_abstract = False
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if t == 'ABSTRACT':
        in_abstract = True
        continue
    if in_abstract:
        if t.startswith('Table of contents') or t.startswith('CHAPTER'):
            break
        if t:
            abstract_paras.append(p)

ABSTRACT_LINES = [
    ("The YouTube Data Analysis System is a data analysis project developed to explore and "
     "analyze the India YouTube Trending Videos dataset. The project uses Python and the "
     "Pandas library in Google Colab to clean, preprocess, analyze, and visualize YouTube "
     "trending video data."),

    ("The original dataset, INvideos.csv, contains information about trending YouTube videos "
     "in India, including video IDs, titles, channel names, category IDs, publish time, "
     "trending date, views, likes, dislikes, and comment counts. After data cleaning and "
     "preprocessing, the final processed dataset contains 33,089 records and 16 columns."),

    ("The project performs exploratory data analysis to understand the distribution and "
     "patterns in the dataset. The analysis covers channel-wise performance, category-wise "
     "video distribution and views, video popularity based on views and likes, publishing "
     "time analysis across year, month, day and hour, and engagement analysis using likes "
     "and comment counts."),

    ("Derived features including publish_year, publish_month, publish_day, publish_hour, "
     "engagement (likes + comment_count), and engagement_rate ((engagement / views) \u00d7 100) "
     "are calculated to support deeper analysis. The processed dataset is exported as "
     "youtube_dashboard_data.csv."),

    ("The project also includes an interactive React/Vite dashboard that loads the processed "
     "CSV dataset and presents the analytical results through dynamic charts, tables, filters, "
     "and key performance indicators. The dashboard provides a premium dark glassmorphism "
     "interface with views trend charts, channel leaderboards, category breakdowns, engagement "
     "analysis, and publishing-time insights."),

    ("The project demonstrates the practical application of data analysis techniques on "
     "real-world social media data. It provides meaningful insights about video popularity, "
     "channel performance, category trends, and engagement patterns. The system can be "
     "further extended with real-time data integration and predictive analytics in the future."),
]

for idx, new_text in enumerate(ABSTRACT_LINES):
    if idx < len(abstract_paras):
        update_para(abstract_paras[idx], new_text)
    # extra old abstract paragraphs: blank them
for idx in range(len(ABSTRACT_LINES), len(abstract_paras)):
    clear_para(abstract_paras[idx])

# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 – Chapter 1: Introduction
# ─────────────────────────────────────────────────────────────────────────────

CH1_MAP = {
    '1.1 Introduction to the Project': None,  # heading – keep
    'Employee attendance and salary management are important':
        ('YouTube is one of the largest video-sharing platforms in the world, generating enormous '
         'amounts of data every day. Among the most valuable publicly available datasets is the '
         'YouTube Trending Videos dataset, which contains information about videos that appeared '
         'on the trending page in India. This dataset includes video titles, channel names, '
         'categories, publish time, trending date, views, likes, dislikes, and comment counts.'),

    'Traditional methods of analyzing employee records':
        ('Traditional methods of analyzing such large social media datasets generally depend on '
         'manual spreadsheet examination, which is time-consuming and error-prone. When the '
         'dataset contains tens of thousands of records, meaningful patterns are difficult to '
         'identify without systematic data analysis tools.'),

    'The Employee Attendance and Salary Analysis System uses data analysis':
        ('The YouTube Data Analysis System uses data analysis techniques and Python/Pandas to '
         'convert the raw INvideos.csv dataset into useful insights. The project cleans, '
         'preprocesses, and analyzes the dataset to identify patterns in video popularity, '
         'channel performance, category distribution, publishing behavior, and audience engagement.'),

    'The project analyzes employee attendance and salary information':
        ('The project analyzes YouTube trending video data and presents the results using '
         'meaningful charts, statistics, and an interactive React/Vite dashboard. This makes '
         'the analytical results easier for end users to explore and understand.'),
}

CH1_PROBLEM = [
    ('YouTube generates large amounts of video-related trending data. '
     'Manually analyzing this information to extract meaningful patterns is '
     'time-consuming and impractical for large datasets.'),

    'It can also be difficult to identify:',
    'Videos with the highest number of views.',
    'Videos with the highest likes and comments.',
    'Channels with the most trending videos.',
    'Category-wise distribution of trending videos.',
    'Publishing-time patterns that correlate with high viewership.',
    'Engagement patterns and rates across the dataset.',
    'Trends in views, likes, and comments over time.',
    ('Therefore, there is a need for a data analysis system that can process YouTube '
     'trending video information and present the results in a structured, visual, '
     'and interactive format.'),
]

CH1_OBJECTIVES = [
    'The main objectives of the project are:',
    'To understand the structure and content of the INvideos.csv dataset.',
    'To clean and preprocess the dataset for analysis.',
    'To analyze video views, likes, dislikes, and comment counts.',
    'To identify the top trending channels and videos.',
    'To perform category-wise analysis of trending videos.',
    'To study publishing-time patterns across year, month, day, and hour.',
    'To calculate engagement and engagement rate for each video.',
    'To represent the analysis results using different visualization techniques.',
    'To build an interactive React/Vite dashboard connected to the processed CSV.',
    'To generate meaningful insights from the analyzed YouTube dataset.',
]

CH1_SCOPE_INTRO = [
    'The scope of the project includes YouTube trending video data analysis, '
    'channel analysis, category analysis, and publishing-time analysis.',
    'The project covers:',
]
CH1_SCOPE_ITEMS = [
    'YouTube trending video analysis.',
    'Channel performance analysis.',
    'Category distribution analysis.',
    'Video views analysis.',
    'Video likes analysis.',
    'Video comment analysis.',
    'Engagement and engagement rate analysis.',
    'Publishing-time analysis (year, month, day, hour).',
    'Statistical analysis.',
    'Data visualization.',
    'Interactive dashboard presentation.',
    'Insight generation from the processed dataset.',
    ('The system can also be extended in the future to include real-time YouTube API '
     'integration, automated dataset updates, predictive analytics, and trend forecasting.'),
]

def update_ch1(doc):
    paras = doc.paragraphs
    n = len(paras)

    # Locate Chapter 1 block
    ch1_start = find_para_index(doc, 'CHAPTER 1')
    ch1_end = find_para_index(doc, 'CHAPTER 2')
    if ch1_start < 0:
        return

    ch1_paras = paras[ch1_start:ch1_end if ch1_end > 0 else ch1_start + 80]

    # Rewrite intro paras
    INTRO_REWRITES = [
        (['Employee attendance and salary management', 'video management are important activities'],
         ('YouTube is one of the largest video-sharing platforms in the world, generating '
          'enormous amounts of data every day. Among the most valuable publicly available '
          'datasets is the YouTube Trending Videos dataset, which contains information about '
          'videos that appeared on the trending page in India. This dataset includes video '
          'titles, channel names, categories, publish time, trending date, views, likes, '
          'dislikes, and comment counts.')),

        (['Traditional methods of analyzing employee', 'Traditional methods of analyzing such large'],
         ('Traditional methods of analyzing such large social media datasets generally depend '
          'on manual spreadsheet examination, which is time-consuming and error-prone. When '
          'the dataset contains tens of thousands of records, meaningful patterns are difficult '
          'to identify without systematic data analysis tools.')),

        (['The Employee Attendance and Salary Analysis System uses data analysis', 'uses data analysis techniques to convert raw employee records'],
         ('The YouTube Data Analysis System uses data analysis techniques and Python/Pandas '
          'to convert the raw INvideos.csv dataset into useful insights. The project cleans, '
          'preprocesses, and analyzes the dataset to identify patterns in video popularity, '
          'channel performance, category distribution, publishing behavior, and audience '
          'engagement.')),

        (['The project analyzes employee attendance and salary information', 'The project analyzes YouTube trending video information and presents the results using meaningful graphs'],
         ('The project analyzes YouTube trending video data and presents the results using '
          'meaningful charts, statistics, and an interactive React/Vite dashboard. This makes '
          'the analytical results easier for end users to explore and understand.')),
    ]

    for p in ch1_paras:
        t = p.text.strip()
        for needles, replacement in INTRO_REWRITES:
            if any(n.lower() in t.lower() for n in needles):
                update_para(p, replacement)
                break

    # 1.2 Problem Statement
    prob_items_idx = 0
    in_problem = False
    problem_list_paras = []
    for p in ch1_paras:
        t = p.text.strip()
        if '1.2 Problem Statement' in t:
            in_problem = True
            continue
        if in_problem and '1.3 Objectives' in t:
            break
        if in_problem and t:
            problem_list_paras.append(p)

    PROBLEM_LINES = [
        ('YouTube generates large amounts of video-related trending data. '
         'Manually analyzing this information to extract meaningful patterns is '
         'time-consuming and impractical for large datasets.'),
        'It can also be difficult to identify:',
        'Videos with the highest number of views.',
        'Videos with the highest likes and comments.',
        'Channels with the most trending videos.',
        'Category-wise distribution of trending videos.',
        'Publishing-time patterns within the dataset.',
        'Engagement patterns and rates across the dataset.',
        'Trends in views, likes, and comments over time.',
        ('Therefore, there is a need for a data analysis system that can process '
         'YouTube trending video information and present the results in a '
         'structured, visual, and interactive format.'),
    ]
    for idx, line in enumerate(PROBLEM_LINES):
        if idx < len(problem_list_paras):
            update_para(problem_list_paras[idx], line)
    for idx in range(len(PROBLEM_LINES), len(problem_list_paras)):
        clear_para(problem_list_paras[idx])

    # 1.3 Objectives
    obj_paras = []
    in_obj = False
    for p in ch1_paras:
        t = p.text.strip()
        if '1.3 Objectives' in t:
            in_obj = True
            continue
        if in_obj and '1.4 Scope' in t:
            break
        if in_obj and t:
            obj_paras.append(p)

    OBJ_LINES = [
        'The main objectives of the project are:',
        'To understand the structure and content of the INvideos.csv dataset.',
        'To clean and preprocess the dataset for analysis.',
        'To analyze video views, likes, dislikes, and comment counts.',
        'To identify the top trending channels and videos.',
        'To perform category-wise analysis of trending videos.',
        'To study publishing-time patterns across year, month, day, and hour.',
        'To calculate engagement and engagement rate for each video.',
        'To represent the analysis results using different visualization techniques.',
        'To build an interactive React/Vite dashboard connected to the processed CSV.',
        'To generate meaningful insights from the analyzed YouTube dataset.',
    ]
    for idx, line in enumerate(OBJ_LINES):
        if idx < len(obj_paras):
            update_para(obj_paras[idx], line)
    for idx in range(len(OBJ_LINES), len(obj_paras)):
        clear_para(obj_paras[idx])

    # 1.4 Scope
    scope_paras = []
    in_scope = False
    for p in ch1_paras:
        t = p.text.strip()
        if '1.4 Scope' in t:
            in_scope = True
            continue
        if in_scope and 'CHAPTER 2' in t:
            break
        if in_scope and t:
            scope_paras.append(p)

    SCOPE_LINES = [
        ('The scope of the project includes YouTube trending video data analysis, '
         'channel analysis, category analysis, and publishing-time analysis.'),
        'The project covers:',
        'YouTube trending video analysis.',
        'Channel performance analysis.',
        'Category distribution analysis.',
        'Video views analysis.',
        'Video likes analysis.',
        'Video comment analysis.',
        'Engagement and engagement rate analysis.',
        'Publishing-time analysis (year, month, day, hour).',
        'Statistical analysis.',
        'Data visualization.',
        'Interactive dashboard presentation.',
        'Insight generation from the processed dataset.',
        ('The system can also be extended in the future to include real-time YouTube API '
         'integration, automated dataset updates, predictive analytics, and trend forecasting.'),
    ]
    for idx, line in enumerate(SCOPE_LINES):
        if idx < len(scope_paras):
            update_para(scope_paras[idx], line)
    for idx in range(len(SCOPE_LINES), len(scope_paras)):
        clear_para(scope_paras[idx])

update_ch1(doc)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 7 – Chapter 2: Dataset Description
# ─────────────────────────────────────────────────────────────────────────────

def update_ch2(doc):
    ch2_start = find_para_index(doc, 'CHAPTER 2')
    ch3_start = find_para_index(doc, 'CHAPTER 3')
    if ch2_start < 0:
        return

    ch2_paras = doc.paragraphs[ch2_start: ch3_start if ch3_start > 0 else ch2_start + 100]

    SECTION_MAP = {
        '2.1 Dataset Source': [
            'The dataset used is the India YouTube Trending Videos dataset (INvideos.csv).',
            'It contains information about trending YouTube videos in India, including video details, views, likes, and comments.',
            'The project uses this dataset to perform exploratory data analysis and build an interactive dashboard.',
        ],
        '2.2 Dataset Description': [
            'The data is cleaned and preprocessed. The following columns are used:',
            'Video Information: video_id, trending_date, title, channel_title, category_id, publish_time',
            'Interaction Metrics: views, likes, dislikes, comment_count',
            'Derived Features: publish_year, publish_month, publish_day, publish_hour, engagement, engagement_rate',
            'Original unused columns (e.g., tags, thumbnail_link, description) were excluded.',
        ],
        '2.3 Features / Attributes': [
            'The attributes are categorized into core information and derived metrics.',
        ],
        '2.4 Target Variable, if Applicable': [
            'This is a descriptive data analysis project, so there is no target variable for prediction.',
            'The focus is on understanding engagement patterns and trending behavior.',
        ],
        '2.5 Dataset Statistics / Initial Exploration': [
            'Initial exploration included displaying rows (df.head, df.tail), checking data types (df.info), and identifying missing/duplicate values.',
            'The final processed dataset contains 33,089 records and 16 columns.',
        ],
    }

    current_section = None
    section_paras = {}
    section_order = []

    for p in ch2_paras:
        t = p.text.strip()
        matched = None
        for key in SECTION_MAP:
            if key in t:
                matched = key
                break
        if matched:
            current_section = matched
            section_paras[matched] = []
            section_order.append(matched)
        elif current_section and t and not any(hdr in t for hdr in ['CHAPTER', 'DATASET DESCRIPTION']):
            section_paras[current_section].append(p)

    for section_key, lines in SECTION_MAP.items():
        if section_key not in section_paras:
            continue
        paras_to_fill = section_paras[section_key]
        for idx, line in enumerate(lines):
            if idx < len(paras_to_fill):
                update_para(paras_to_fill[idx], line)
        for idx in range(len(lines), len(paras_to_fill)):
            clear_para(paras_to_fill[idx])

update_ch2(doc)

# Update Table 3 (Original 10 Attributes) & Table 4 (6 Derived Features)
if len(doc.tables) > 3:
    t3 = doc.tables[3]
    while len(t3.rows) > 1:
        tbl = t3._tbl
        tbl.remove(t3.rows[-1]._tr)
    # Header
    for c_idx, h in enumerate(["Attribute", "Description"]):
        p = t3.rows[0].cells[c_idx].paragraphs[0]
        clear_para(p)
        r = p.add_run(h)
        r.bold = True
    ORIGINAL_ATTRS = [
        ("video_id",         "Unique identifier for each YouTube video"),
        ("trending_date",    "Date when the video appeared on trending page (format: YY.DD.MM)"),
        ("title",            "Title of the YouTube video"),
        ("channel_title",    "Name of the YouTube channel that published the video"),
        ("category_id",      "Numeric category ID representing the video category"),
        ("publish_time",     "Date and time when the video was originally published"),
        ("views",            "Total view count of the video"),
        ("likes",            "Total number of likes on the video"),
        ("dislikes",         "Total number of dislikes on the video"),
        ("comment_count",    "Total number of comments on the video"),
    ]
    for attr, desc in ORIGINAL_ATTRS:
        row = t3.add_row()
        p0 = row.cells[0].paragraphs[0]
        update_para(p0, attr)
        p1 = row.cells[1].paragraphs[0]
        update_para(p1, desc)

if len(doc.tables) > 4:
    t4 = doc.tables[4]
    while len(t4.rows) > 1:
        tbl = t4._tbl
        tbl.remove(t4.rows[-1]._tr)
    # Header
    for c_idx, h in enumerate(["Derived Attribute", "Description / Formula"]):
        p = t4.rows[0].cells[c_idx].paragraphs[0]
        clear_para(p)
        r = p.add_run(h)
        r.bold = True
    DERIVED_ATTRS = [
        ("publish_year",     "Derived: Year extracted from publish_time"),
        ("publish_month",    "Derived: Month extracted from publish_time"),
        ("publish_day",      "Derived: Day of week extracted from publish_time"),
        ("publish_hour",     "Derived: Hour extracted from publish_time"),
        ("engagement",       "Derived: Total engagement calculated as likes + comment_count"),
        ("engagement_rate",  "Derived: Percentage engagement calculated as (engagement / views) * 100"),
    ]
    for attr, desc in DERIVED_ATTRS:
        row = t4.add_row()
        p0 = row.cells[0].paragraphs[0]
        update_para(p0, attr)
        p1 = row.cells[1].paragraphs[0]
        update_para(p1, desc)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 8 – Chapter 3: Data Preprocessing
# ─────────────────────────────────────────────────────────────────────────────

def update_ch3(doc):
    ch3_start = find_para_index(doc, 'CHAPTER 3')
    ch4_start = find_para_index(doc, 'CHAPTER 4')
    if ch3_start < 0:
        return
    ch3_paras = doc.paragraphs[ch3_start: ch4_start if ch4_start > 0 else ch3_start + 120]

    SECTION_CONTENT = {
        '3.1 Data Collection / Loading': {
            'intro': [
                ('The original dataset is loaded into the Python environment in Google Colab '
                 'using the Pandas library.'),
                'Example:',
                'import pandas as pd',
                '',
                'df = pd.read_csv("INvideos.csv")',
                '',
                'print(df.head())',
                'print(df.shape)',
                ('After loading the dataset, the structure and data types are checked '
                 'to understand the data before performing analysis.'),
            ]
        },
        '3.2 Handling Missing Values': {
            'intro': [
                ('Missing values can affect statistical calculations and visualization. '
                 'Therefore, missing values are identified using:'),
                'df.isnull().sum()',
                ('The INvideos.csv dataset was checked for missing values in all columns. '
                 'The dataset did not contain significant missing values in the primary '
                 'numerical columns used for analysis.'),
            ]
        },
        '3.3 Handling Duplicate / Inconsistent Data': {
            'intro': [
                'Duplicate records are identified using:',
                'df.duplicated().sum()',
                ('The dataset was also checked for repeated video IDs to identify videos '
                 'that appeared on the trending page on multiple dates.'),
                ('Invalid video IDs containing the value #NAME? were identified and '
                 'handled appropriately during data cleaning.'),
                ('Exact duplicate rows were removed using:'),
                'df = df.drop_duplicates()',
                ('After removing exact duplicate rows, the dataset retained 33,089 '
                 'clean records for analysis.'),
            ]
        },
        '3.4 Feature Scaling': {
            'intro': [
                ('Feature scaling is used when numerical variables have significantly '
                 'different ranges and when machine-learning algorithms require comparable '
                 'scales.'),
                ('For this descriptive data analysis project, feature scaling was not '
                 'required because the project does not involve machine-learning model '
                 'training. Statistical and graphical analysis can be performed directly '
                 'on the original numerical values.'),
            ]
        },
        '3.5 Standardization': {
            'intro': [
                ('Standardization transforms numerical variables so that they have a '
                 'common scale.'),
                'The standardization formula is:',
                'Z = (X - mean) / std',
                'where:',
                'X = Original value',
                'mean = Mean of the column',
                'std = Standard deviation of the column',
                ('Standardization is mainly useful when a machine-learning model requires '
                 'standardized numerical features. Since this project is a descriptive '
                 'analysis project, standardization was not applied to the dataset.'),
            ]
        },
        '3.6 Label Encoding': {
            'intro': [
                'Label encoding converts categorical values into numerical labels.',
                ('In this project, the category_id column already contains numerical '
                 'identifiers. Therefore, label encoding was not required for the '
                 'core analysis.'),
                ('Label encoding is mainly useful when categorical information needs '
                 'to be supplied to a machine-learning algorithm.'),
            ]
        },
        '3.7 One-Hot Encoding': {
            'intro': [
                ('One-hot encoding converts categorical variables into separate binary columns.'),
                ('For example, if a category column contains Entertainment, Music, and '
                 'Comedy, one-hot encoding creates separate columns for these categories.'),
                'Example:',
                'df_encoded = pd.get_dummies(df, columns=["category_id"])',
                ('One-hot encoding was not required for the core descriptive analysis '
                 'performed in this project since group-by operations work directly '
                 'with categorical column values.'),
            ]
        },
        '3.8 Other Project-Specific Preprocessing': {
            'intro': [
                'Project-specific preprocessing includes:',
                ('Converting the trending_date column to proper date format. '
                 'The original format used in the dataset was YY.DD.MM, for example '
                 '17.14.11, which required the format string %y.%d.%m during conversion:'),
                'df["trending_date"] = pd.to_datetime(df["trending_date"], format="%y.%d.%m")',
                ('Converting the publish_time column to datetime format:'),
                'df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")',
                ('Extracting derived date and time features:'),
                'df["publish_year"]  = df["publish_time"].dt.year',
                'df["publish_month"] = df["publish_time"].dt.month_name()',
                'df["publish_day"]   = df["publish_time"].dt.day_name()',
                'df["publish_hour"]  = df["publish_time"].dt.hour',
                ('Calculating engagement:'),
                'df["engagement"] = df["likes"] + df["comment_count"]',
                ('Calculating engagement rate:'),
                'df["engagement_rate"] = (df["engagement"] / df["views"]) * 100',
                ('Selecting only the useful columns for the final analysis dataframe:'),
                ('youtube_df = df[["video_id", "trending_date", "title", "channel_title",\n'
                 '                  "category_id", "publish_time", "views", "likes",\n'
                 '                  "dislikes", "comment_count", "publish_year",\n'
                 '                  "publish_month", "publish_day", "publish_hour",\n'
                 '                  "engagement", "engagement_rate"]]'),
                ('Exporting the cleaned and processed dataset:'),
                'youtube_df.to_csv("youtube_dashboard_data.csv", index=False)',
                ('The project methodology specifically identifies trending_date conversion, '
                 'publish_time conversion, derived feature creation, engagement calculation, '
                 'and CSV export as the core preprocessing steps.'),
            ]
        },
    }

    current_section = None
    section_paras = {}

    for p in ch3_paras:
        t = p.text.strip()
        for key in SECTION_CONTENT:
            if key in t:
                current_section = key
                section_paras[key] = []
                break
        else:
            if current_section and t and not any(h in t for h in ['CHAPTER', 'DATA PREPROCESSING']):
                section_paras[current_section].append(p)

    for key, content in SECTION_CONTENT.items():
        if key not in section_paras:
            continue
        lines = content['intro']
        paras = section_paras[key]
        for idx, line in enumerate(lines):
            if idx < len(paras):
                if line == '[INSERT_ARCH_TABLE]':
                    clear_para(paras[idx])
                    arch_steps = ['INvideos.csv', '↓', 'Python / Google Colab', '↓', 'Pandas Data Processing', '↓', 'Data Cleaning', '↓', 'Feature Engineering', '↓', 'Exploratory Data Analysis', '↓', 'Statistical Analysis', '↓', 'Data Visualization', '↓', 'youtube_dashboard_data.csv', '↓', 'React / Vite Dashboard', '↓', 'Insights']
                    insert_single_col_table(paras[idx], arch_steps)
                elif line == '[INSERT_FLOW_TABLE]':
                    clear_para(paras[idx])
                    flow_steps = ['START', '↓', 'Load INvideos.csv', '↓', 'Dataset Exploration', '↓', 'Missing / Duplicate Check', '↓', 'Data Cleaning & Formatting', '↓', 'Feature Engineering', '↓', 'Exploratory Data Analysis', '↓', 'Statistical Analysis', '↓', 'Data Visualization', '↓', 'Export CSV', '↓', 'React Dashboard', '↓', 'END']
                    insert_single_col_table(paras[idx], flow_steps)
                else:
                    update_para(paras[idx], line)
        for idx in range(len(lines), len(paras)):
            clear_para(paras[idx])

update_ch3(doc)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 9 – Chapter 4: System Design and Methodology
# ─────────────────────────────────────────────────────────────────────────────


def insert_single_col_table(ref_para, items):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt
    table = doc.add_table(rows=len(items), cols=1)
    table.style = 'Table Grid'
    for i, item in enumerate(items):
        cell = table.cell(i, 0)
        cell.text = item
        # Center align and set font
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(11)
    # Move table to after ref_para
    ref_para._p.addnext(table._tbl)


def update_ch4(doc):
    ch4_start = find_para_index(doc, 'CHAPTER 4')
    ch5_start = find_para_index(doc, 'CHAPTER 5')
    if ch4_start < 0:
        return
    ch4_paras = doc.paragraphs[ch4_start: ch5_start if ch5_start > 0 else ch4_start + 180]

    METH_FLOW = [
        'The project follows a systematic data analysis methodology.',
        'Data Loading → Data Exploration → Data Cleaning → Data Preprocessing → Feature Engineering → EDA → Visualization → Dashboard → Insights'
    ]

    ARCH_FLOW = [
        'The system architecture follows a sequential data processing pipeline:',
        '[INSERT_ARCH_TABLE]'
    ]

    FLOWCHART = [
        'The flowchart for the data analysis process is as follows:',
        '[INSERT_FLOW_TABLE]'
    ]

    ALGO_SECTION = [
        'The primary approach used is Exploratory Data Analysis (EDA) and descriptive statistics.',
        'The analysis uses group-by operations, sorting, percentage calculations, and time-based aggregation to extract patterns.',
    ]

    current_section = None
    sec_paras = {}

    for p in ch4_paras:
        t = p.text.strip()
        if '4.1 Proposed Methodology' in t:
            current_section = '4.1'
            sec_paras['4.1'] = []
        elif '4.2 System Workflow' in t:
            current_section = '4.2'
            sec_paras['4.2'] = []
        elif '4.3 Flowchart' in t:
            current_section = '4.3'
            sec_paras['4.3'] = []
        elif '4.4 Tools and Technologies' in t:
            current_section = '4.4'
            sec_paras['4.4'] = []
        elif '4.5 Algorithm' in t:
            current_section = '4.5'
            sec_paras['4.5'] = []
        elif current_section and t and not any(h in t for h in ['CHAPTER', 'SYSTEM DESIGN']):
            sec_paras.setdefault(current_section, []).append(p)

    MAP = {
        '4.1': METH_FLOW,
        '4.2': ARCH_FLOW,
        '4.3': FLOWCHART,
        '4.5': ALGO_SECTION,
    }

    for key, lines in MAP.items():
        if key not in sec_paras:
            continue
        paras = sec_paras[key]
        for idx, line in enumerate(lines):
            if idx < len(paras):
                if line == '[INSERT_ARCH_TABLE]':
                    clear_para(paras[idx])
                    arch_steps = ['INvideos.csv', '↓', 'Python / Google Colab', '↓', 'Pandas Data Processing', '↓', 'Data Cleaning', '↓', 'Feature Engineering', '↓', 'Exploratory Data Analysis', '↓', 'Statistical Analysis', '↓', 'Data Visualization', '↓', 'youtube_dashboard_data.csv', '↓', 'React / Vite Dashboard', '↓', 'Insights']
                    insert_single_col_table(paras[idx], arch_steps)
                elif line == '[INSERT_FLOW_TABLE]':
                    clear_para(paras[idx])
                    flow_steps = ['START', '↓', 'Load INvideos.csv', '↓', 'Dataset Exploration', '↓', 'Missing / Duplicate Check', '↓', 'Data Cleaning & Formatting', '↓', 'Feature Engineering', '↓', 'Exploratory Data Analysis', '↓', 'Statistical Analysis', '↓', 'Data Visualization', '↓', 'Export CSV', '↓', 'React Dashboard', '↓', 'END']
                    insert_single_col_table(paras[idx], flow_steps)
                else:
                    update_para(paras[idx], line)
        for idx in range(len(lines), len(paras)):
            clear_para(paras[idx])

update_ch4(doc)

# Update Tools table (Table 5)

tools_table = None
for t in doc.tables:
    if len(t.rows) > 0 and len(t.columns) == 2:
        try:
            if 'Python' in t.rows[0].cells[0].text or 'Language' in t.rows[0].cells[0].text or 'Technology' in t.rows[0].cells[0].text:
                tools_table = t
        except:
            pass
        if tools_table is None and 'Attribute' not in t.rows[0].cells[0].text and 'Derived Attribute' not in t.rows[0].cells[0].text:
            if 'Tool' in t.rows[0].cells[0].text or 'Technology' in t.rows[0].cells[0].text:
                tools_table = t

if tools_table:

    while len(tools_table.rows) > 1:
        tbl = tools_table._tbl
        tbl.remove(tools_table.rows[-1]._tr)

    TOOLS = [
        ("Python",                  "Data processing and analysis"),
        ("Google Colab",            "Cloud-based notebook environment"),
        ("Pandas",                  "Data loading, cleaning, preprocessing, and analysis"),
        ("Matplotlib",              "Data visualization and chart generation"),
        ("CSV",                     "Data storage format for the dataset"),
        ("React",                   "JavaScript library for building the dashboard UI"),
        ("Vite",                    "Build tool and development server for the dashboard"),
        ("JavaScript / JSX",        "Dashboard logic and component development"),
        ("PapaParse",               "CSV parsing library used in the React dashboard"),
        ("Recharts",                "Chart components for the React dashboard"),
        ("Tailwind CSS / CSS",      "Dashboard styling and glassmorphism design"),
    ]
    for tool, purpose in TOOLS:
        row = tools_table.add_row()
        row.cells[0].text = tool
        row.cells[1].text = purpose

# ─────────────────────────────────────────────────────────────────────────────
# STEP 10 – Chapter 5: Implementation
# ─────────────────────────────────────────────────────────────────────────────

def update_ch5(doc):
    ch5_start = find_para_index(doc, 'CHAPTER 5')
    ch6_start = find_para_index(doc, 'CHAPTER 6')
    if ch5_start < 0:
        return
    ch5_paras = doc.paragraphs[ch5_start: ch6_start if ch6_start > 0 else ch5_start + 150]

    IMPL_MAP = {
        '5.1 Development Environment': [
            ('The project is implemented using Google Colab as the primary development '
             'environment. Google Colab provides a cloud-based Python notebook environment '
             'that does not require local installation.'),
            'The main programming language used is Python.',
            'The important Python libraries used are:',
            'import pandas as pd',
            'import matplotlib.pyplot as plt',
            ('The interactive dashboard is developed using React and Vite. The dashboard '
             'loads the processed CSV file directly using PapaParse and renders dynamic '
             'charts and tables for the end user.'),
        ],
        '5.2 Dataset Loading and Exploration': [
            'The dataset is loaded using Pandas.',
            'import pandas as pd',
            '',
            'df = pd.read_csv("INvideos.csv")',
            '',
            'print(df.head())',
            'print(df.shape)',
            'print(df.info())',
            'Initial exploration is performed to understand the dataset structure.',
            'Important operations include:',
            'df.head()',
            'df.tail()',
            'df.shape',
            'df.columns',
            'df.info()',
            'df.describe()',
            'df.isnull().sum()',
            'df.duplicated().sum()',
        ],
        '5.3 Preprocessing Implementation': [
            'The preprocessing stage includes:',
            '# Check missing values',
            'print(df.isnull().sum())',
            '',
            '# Remove exact duplicate rows',
            'df = df.drop_duplicates()',
            '',
            '# Convert trending_date (format: YY.DD.MM)',
            'df["trending_date"] = pd.to_datetime(df["trending_date"], format="%y.%d.%m")',
            '',
            '# Convert publish_time',
            'df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")',
            '',
            '# Extract date/time features',
            'df["publish_year"]  = df["publish_time"].dt.year',
            'df["publish_month"] = df["publish_time"].dt.month_name()',
            'df["publish_day"]   = df["publish_time"].dt.day_name()',
            'df["publish_hour"]  = df["publish_time"].dt.hour',
            '',
            '# Calculate engagement',
            'df["engagement"] = df["likes"] + df["comment_count"]',
            '',
            '# Calculate engagement rate',
            'df["engagement_rate"] = (df["engagement"] / df["views"]) * 100',
            '',
            ('Additional preprocessing includes handling invalid #NAME? video IDs '
             'and selecting only the useful columns for the analysis dataframe.'),
        ],
        '5.4 Exploratory Data Analysis': [
            ('Exploratory Data Analysis is performed to understand the major patterns '
             'in the YouTube trending data.'),
            'The analysis includes:',
            'Channel Analysis',
            'Most frequently trending channels.',
            'Top channels by total views.',
            'Top channels by total likes.',
            'Video Views Analysis',
            'Top videos by total view count.',
            'Distribution of views across categories.',
            'Views trend over time.',
            'Likes Analysis',
            'Top videos by total likes.',
            'Distribution of likes across categories.',
            'Comment Analysis',
            'Top videos by comment count.',
            'Distribution of comments across categories.',
            'Category Analysis',
            'Number of trending videos per category.',
            'Category-wise total views.',
            'Category-wise average views.',
            'Publishing-Time Analysis',
            'Number of videos published per year.',
            'Number of videos published per month.',
            'Number of videos published per day of week.',
            'Number of videos published per hour.',
            'Engagement Analysis',
            'Distribution of engagement values.',
            'Distribution of engagement rates.',
            'Top videos by engagement rate.',
        ],
        '5.5 Model / Analysis Implementation': [
            ('Since the main project is a descriptive data analysis project, the '
             'implementation focuses on statistical and exploratory analysis.'),
            'For example:',
            'print(df["views"].mean())',
            'print(df["views"].median())',
            'print(df["likes"].mean())',
            'Channel-wise analysis can be performed using:',
            'df.groupby("channel_title")["views"].sum().sort_values(ascending=False)',
            'Category-wise analysis can be performed using:',
            'df.groupby("category_id")["views"].sum().sort_values(ascending=False)',
            'Top videos by views:',
            'df.sort_values("views", ascending=False).head(10)',
        ],
        '5.6 Important Code Explanation': [
            'Reading Dataset',
            'df = pd.read_csv("INvideos.csv")',
            'This statement loads the CSV dataset into a Pandas DataFrame.',
            'Checking Dataset Size',
            'df.shape',
            'It returns the number of rows and columns in the dataset.',
            'Checking Missing Values',
            'df.isnull().sum()',
            'It displays the number of missing values in each column.',
            'Removing Duplicates',
            'df.drop_duplicates()',
            'It removes exact duplicate rows from the dataset.',
            'Grouping Data',
            'df.groupby("channel_title")["views"].sum()',
            'It calculates the total views for each channel.',
            'Calculating Engagement',
            'df["engagement"] = df["likes"] + df["comment_count"]',
            'It calculates the total engagement for each video record.',
            'Calculating Engagement Rate',
            'df["engagement_rate"] = (df["engagement"] / df["views"]) * 100',
            'It calculates the engagement rate as a percentage of views.',
        ],
    }

    current_section = None
    sec_paras = {}

    for p in ch5_paras:
        t = p.text.strip()
        matched = None
        for key in IMPL_MAP:
            if key in t:
                matched = key
                break
        if matched:
            current_section = matched
            sec_paras[matched] = []
        elif current_section and t and not any(h in t for h in ['CHAPTER', 'IMPLEMENTATION']):
            sec_paras[current_section].append(p)

    for key, lines in IMPL_MAP.items():
        if key not in sec_paras:
            continue
        paras = sec_paras[key]
        for idx, line in enumerate(lines):
            if idx < len(paras):
                if line == '[INSERT_ARCH_TABLE]':
                    clear_para(paras[idx])
                    arch_steps = ['INvideos.csv', '↓', 'Python / Google Colab', '↓', 'Pandas Data Processing', '↓', 'Data Cleaning', '↓', 'Feature Engineering', '↓', 'Exploratory Data Analysis', '↓', 'Statistical Analysis', '↓', 'Data Visualization', '↓', 'youtube_dashboard_data.csv', '↓', 'React / Vite Dashboard', '↓', 'Insights']
                    insert_single_col_table(paras[idx], arch_steps)
                elif line == '[INSERT_FLOW_TABLE]':
                    clear_para(paras[idx])
                    flow_steps = ['START', '↓', 'Load INvideos.csv', '↓', 'Dataset Exploration', '↓', 'Missing / Duplicate Check', '↓', 'Data Cleaning & Formatting', '↓', 'Feature Engineering', '↓', 'Exploratory Data Analysis', '↓', 'Statistical Analysis', '↓', 'Data Visualization', '↓', 'Export CSV', '↓', 'React Dashboard', '↓', 'END']
                    insert_single_col_table(paras[idx], flow_steps)
                else:
                    update_para(paras[idx], line)
        for idx in range(len(lines), len(paras)):
            clear_para(paras[idx])

update_ch5(doc)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 11 – Chapter 6: Data Visualization and Results
# ─────────────────────────────────────────────────────────────────────────────

def update_ch6(doc):
    ch6_start = find_para_index(doc, 'CHAPTER 6')
    ch7_start = find_para_index(doc, 'CHAPTER 7')
    if ch6_start < 0:
        return
    ch6_paras = doc.paragraphs[ch6_start: ch7_start if ch7_start > 0 else ch6_start + 150]

    VIZ_MAP = {
        '6.1 Bar Graph': [
            'A bar graph is used to compare categorical data.',
            ('For example, the top 10 channels by trending video count can be '
             'visualized using:'),
            'top_channels = df["channel_title"].value_counts().head(10)',
            '',
            'top_channels.plot(kind="bar")',
            '',
            'plt.title("Top 10 Channels by Trending Videos")',
            'plt.xlabel("Channel")',
            'plt.ylabel("Number of Trending Videos")',
            'plt.xticks(rotation=45)',
            'plt.show()',
            ('The bar graph helps compare the number of trending appearances for '
             'different YouTube channels in the dataset.'),
        ],
        '6.2 Pie Chart': [
            ('A pie chart can be used to represent the proportion of trending '
             'videos across different categories.'),
            'category_counts = df["category_id"].value_counts()',
            '',
            'category_counts.plot(',
            '    kind="pie",',
            '    autopct="%1.1f%%"',
            ')',
            '',
            'plt.title("Trending Videos by Category")',
            'plt.ylabel("")',
            'plt.show()',
            ('The chart provides a visual representation of the proportion of '
             'trending videos across different YouTube categories.'),
        ],
        '6.3 Histogram': [
            ('A histogram is used to understand the distribution of numerical '
             'values such as views or engagement rate.'),
            'plt.hist(df["views"], bins=30)',
            '',
            'plt.title("Distribution of Video Views")',
            'plt.xlabel("Views")',
            'plt.ylabel("Frequency")',
            'plt.show()',
            ('The histogram shows how view counts are distributed across '
             'the dataset records.'),
        ],
        '6.4 Box Plot': [
            ('A box plot is useful for understanding the spread of numerical '
             'data and identifying possible outliers.'),
            'plt.boxplot(df["likes"])',
            '',
            'plt.title("Distribution of Video Likes")',
            'plt.show()',
            ('The box plot displays the median, quartiles, spread, and possible '
             'outliers in the likes distribution.'),
        ],
        '6.5 Line Chart': [
            ('A line chart can be used to display trending patterns over time.'),
            'monthly_views = df.groupby("publish_month")["views"].mean()',
            '',
            'monthly_views.plot(kind="line", marker="o")',
            '',
            'plt.title("Average Views by Publish Month")',
            'plt.xlabel("Month")',
            'plt.ylabel("Average Views")',
            'plt.show()',
            ('The line chart helps identify changes or trends across publishing '
             'months in the dataset.'),
        ],
        '6.6 Scatter Plot': [
            ('A scatter plot can be used to analyze the relationship between '
             'two numerical variables.'),
            'For example:',
            'plt.scatter(df["views"], df["likes"])',
            '',
            'plt.title("Views vs Likes")',
            'plt.xlabel("Views")',
            'plt.ylabel("Likes")',
            'plt.show()',
            ('This visualization helps examine whether higher view counts are '
             'associated with higher likes in the dataset.'),
        ],
        '6.7 Project-Specific Visualizations': [
            'The project-specific visualizations include:',
            'Top 10 Channels by Trending Video Count.',
            'Category-wise Trending Video Count.',
            'Category-wise Total Views.',
            'Top Videos by Views.',
            'Top Videos by Likes.',
            'Top Videos by Comments.',
            'Videos Published by Month.',
            'Videos Published by Day of Week.',
            'Videos Published by Hour.',
            'Views vs Likes Scatter Plot.',
            'Views vs Comments Scatter Plot.',
            ('The project specifically identifies channel analysis, category analysis, '
             'views analysis, likes analysis, comments analysis, publishing time analysis, '
             'and engagement analysis as the core visualization areas.'),
        ],
        '6.8 Interpretation of Visualizations': [
            ('The visualizations make the analysis easier to understand.'),
            ('Bar charts help compare channels, categories, and publishing patterns. '
             'Pie charts show proportions of video categories. Histograms show the '
             'distribution of numerical values such as views and engagement rates. '
             'Scatter plots help examine the relationship between views and likes. '
             'Line charts help identify publishing trends over time.'),
            ('The actual interpretation should be based on the graphs generated '
             'from the final youtube_dashboard_data.csv dataset.'),
        ],
    }

    current_section = None
    sec_paras = {}

    for p in ch6_paras:
        t = p.text.strip()
        matched = None
        for key in VIZ_MAP:
            if key in t:
                matched = key
                break
        if matched:
            current_section = matched
            sec_paras[matched] = []
        elif current_section and t and not any(h in t for h in ['CHAPTER', 'DATA VISUALIZATION']):
            sec_paras[current_section].append(p)

    for key, lines in VIZ_MAP.items():
        if key not in sec_paras:
            continue
        paras = sec_paras[key]
        for idx, line in enumerate(lines):
            if idx < len(paras):
                if line == '[INSERT_ARCH_TABLE]':
                    clear_para(paras[idx])
                    arch_steps = ['INvideos.csv', '↓', 'Python / Google Colab', '↓', 'Pandas Data Processing', '↓', 'Data Cleaning', '↓', 'Feature Engineering', '↓', 'Exploratory Data Analysis', '↓', 'Statistical Analysis', '↓', 'Data Visualization', '↓', 'youtube_dashboard_data.csv', '↓', 'React / Vite Dashboard', '↓', 'Insights']
                    insert_single_col_table(paras[idx], arch_steps)
                elif line == '[INSERT_FLOW_TABLE]':
                    clear_para(paras[idx])
                    flow_steps = ['START', '↓', 'Load INvideos.csv', '↓', 'Dataset Exploration', '↓', 'Missing / Duplicate Check', '↓', 'Data Cleaning & Formatting', '↓', 'Feature Engineering', '↓', 'Exploratory Data Analysis', '↓', 'Statistical Analysis', '↓', 'Data Visualization', '↓', 'Export CSV', '↓', 'React Dashboard', '↓', 'END']
                    insert_single_col_table(paras[idx], flow_steps)
                else:
                    update_para(paras[idx], line)
        for idx in range(len(lines), len(paras)):
            clear_para(paras[idx])

update_ch6(doc)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 12 – Chapter 7: Model Evaluation / Analysis of Results
# ─────────────────────────────────────────────────────────────────────────────

def update_ch7(doc):
    ch7_start = find_para_index(doc, 'CHAPTER 7')
    ch8_start = find_para_index(doc, 'CHAPTER 8')
    if ch7_start < 0:
        return
    ch7_paras = doc.paragraphs[ch7_start: ch8_start if ch8_start > 0 else ch7_start + 80]

    CH7_MAP = {
        '7.1 Evaluation Metrics': [
            ('Since the primary project is descriptive and exploratory data analysis, '
             'traditional machine-learning evaluation metrics such as accuracy, precision, '
             'recall, and F1-score are not applicable.'),
            'Instead, the analysis is evaluated using:',
            'Mean',
            'Median',
            'Standard deviation',
            'Minimum and maximum values',
            'Percentages',
            'Group-wise comparisons (channel, category)',
            'Time-based patterns (year, month, day, hour)',
            ('These statistical measures help understand the characteristics and '
             'patterns present in the YouTube trending dataset.'),
        ],
        '7.2 Experimental Results': [
            'The analysis produces results related to:',
            'Total records in the cleaned dataset: 33,089',
            'Total columns in the final dataset: 16',
            'Total views across all records: approximately 32.97 billion',
            'Total likes across all records: approximately 846.67 million',
            'Average views per video: approximately 996,342',
            'Average likes per video: approximately 25,387',
            'Average comments per video: approximately 2,525',
            'Average engagement rate: approximately 2.45%',
            ('Channel-wise analysis: T-Series showed the highest total views among '
             'channels in the analyzed dataset.'),
            ('Channel-wise analysis: Amit Bhadana showed the highest total likes '
             'among the analyzed channel-level results.'),
            ('Video-level analysis: YouTube Rewind 2017 appeared as the most viewed '
             'record in the analyzed dataset.'),
            ('Publishing patterns: Friday had the highest publishing frequency in '
             'this dataset.'),
            ('Publishing patterns: 2 PM had the highest publishing frequency in '
             'this dataset.'),
            ('These results are based on the INvideos.csv dataset. They represent '
             'patterns in the historical trending data and do not represent overall '
             'YouTube statistics.'),
        ],
        '7.3 Result Interpretation': [
            ('The analysis results can be interpreted using the generated tables and graphs.'),
            'For example:',
            ('Channel-wise trending counts show which YouTube channels appeared most '
             'frequently on the trending page in India during the dataset period.'),
            ('Category analysis shows the distribution of trending videos across '
             'different content categories.'),
            ('Views analysis shows the total views accumulated by the most popular '
             'trending videos in the dataset.'),
            ('Publishing-time analysis shows the days and hours with the highest '
             'publishing frequency in the dataset.'),
            ('Engagement analysis shows the relationship between views, likes, and '
             'comments across the trending video records.'),
        ],
        '7.4 Discussion': [
            ('The project demonstrates how data analysis techniques can be applied to '
             'real-world social media trending data.'),
            ('The analysis converts raw INvideos.csv records into meaningful information '
             'through preprocessing, statistical analysis, visualization, and an '
             'interactive dashboard.'),
            ('The results provide insight into YouTube channel performance, category '
             'distribution, video popularity patterns, publishing behavior, and audience '
             'engagement based on the dataset.'),
            ('The project methodology supports data-driven understanding of YouTube '
             'trending patterns rather than relying on manual examination of raw records.'),
        ],
    }

    current_section = None
    sec_paras = {}

    for p in ch7_paras:
        t = p.text.strip()
        matched = None
        for key in CH7_MAP:
            if key in t:
                matched = key
                break
        if matched:
            current_section = matched
            sec_paras[matched] = []
        elif current_section and t and not any(h in t for h in ['CHAPTER', 'MODEL EVALUATION']):
            sec_paras[current_section].append(p)

    for key, lines in CH7_MAP.items():
        if key not in sec_paras:
            continue
        paras = sec_paras[key]
        for idx, line in enumerate(lines):
            if idx < len(paras):
                if line == '[INSERT_ARCH_TABLE]':
                    clear_para(paras[idx])
                    arch_steps = ['INvideos.csv', '↓', 'Python / Google Colab', '↓', 'Pandas Data Processing', '↓', 'Data Cleaning', '↓', 'Feature Engineering', '↓', 'Exploratory Data Analysis', '↓', 'Statistical Analysis', '↓', 'Data Visualization', '↓', 'youtube_dashboard_data.csv', '↓', 'React / Vite Dashboard', '↓', 'Insights']
                    insert_single_col_table(paras[idx], arch_steps)
                elif line == '[INSERT_FLOW_TABLE]':
                    clear_para(paras[idx])
                    flow_steps = ['START', '↓', 'Load INvideos.csv', '↓', 'Dataset Exploration', '↓', 'Missing / Duplicate Check', '↓', 'Data Cleaning & Formatting', '↓', 'Feature Engineering', '↓', 'Exploratory Data Analysis', '↓', 'Statistical Analysis', '↓', 'Data Visualization', '↓', 'Export CSV', '↓', 'React Dashboard', '↓', 'END']
                    insert_single_col_table(paras[idx], flow_steps)
                else:
                    update_para(paras[idx], line)
        for idx in range(len(lines), len(paras)):
            clear_para(paras[idx])

update_ch7(doc)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 13 – Chapter 8: Output Screenshots
# ─────────────────────────────────────────────────────────────────────────────

def update_ch8(doc):
    ch8_start = find_para_index(doc, 'CHAPTER 8')
    ch9_start = find_para_index(doc, 'CHAPTER 9')
    if ch8_start < 0:
        return
    ch8_paras = doc.paragraphs[ch8_start: ch9_start if ch9_start > 0 else ch8_start + 80]

    CH8_MAP = {
        '8.1 Input / Dataset Screenshots': [
            'The following screenshots should be included:',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.1: Original INvideos.csv dataset loaded in Google Colab]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.2: First five rows of the dataset (df.head())]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.3: Dataset structure and column information (df.info())]',
        ],
        '8.2 Preprocessing Outputs': [
            'The following screenshots should be included:',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.4: Missing-value analysis (df.isnull().sum())]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.5: Duplicate-value analysis (df.duplicated().sum())]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.6: Cleaned dataset after removing duplicates]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.7: Processed youtube_dashboard_data.csv with derived features]',
        ],
        '8.3 Visualization Outputs': [
            'The following screenshots should be included:',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.8: Top 10 Channels by Trending Videos \u2013 Bar Chart]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.9: Category-wise Video Count \u2013 Bar Chart]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.10: Category-wise Total Views \u2013 Bar Chart]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.11: Top Videos by Views \u2013 Horizontal Bar Chart]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.12: Videos Published by Month \u2013 Line/Bar Chart]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.13: Videos Published by Day of Week \u2013 Bar Chart]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.14: Videos Published by Hour \u2013 Bar Chart]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.15: Views vs Likes \u2013 Scatter Plot]',
        ],
        '8.4 Prediction / Analysis Outputs': [
            ('Since this is a descriptive data analysis project, machine-learning '
             'prediction screenshots are not applicable in the current implementation.'),
            'Dashboard Screenshots:',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.16: React/Vite Dashboard \u2013 Overview Tab]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.17: Dashboard \u2013 Trending Videos Tab]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.18: Dashboard \u2013 Channels Tab]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.19: Dashboard \u2013 Engagement Tab]',
            '[INSERT SCREENSHOT HERE \u2013 Figure 8.20: Dashboard \u2013 Publishing Insights Tab]',
        ],
    }

    current_section = None
    sec_paras = {}

    for p in ch8_paras:
        t = p.text.strip()
        matched = None
        for key in CH8_MAP:
            if key in t:
                matched = key
                break
        if matched:
            current_section = matched
            sec_paras[matched] = []
        elif current_section and t and not any(h in t for h in ['CHAPTER', 'OUTPUT SCREENSHOTS']):
            sec_paras[current_section].append(p)

    for key, lines in CH8_MAP.items():
        if key not in sec_paras:
            continue
        paras = sec_paras[key]
        for idx, line in enumerate(lines):
            if idx < len(paras):
                if line == '[INSERT_ARCH_TABLE]':
                    clear_para(paras[idx])
                    arch_steps = ['INvideos.csv', '↓', 'Python / Google Colab', '↓', 'Pandas Data Processing', '↓', 'Data Cleaning', '↓', 'Feature Engineering', '↓', 'Exploratory Data Analysis', '↓', 'Statistical Analysis', '↓', 'Data Visualization', '↓', 'youtube_dashboard_data.csv', '↓', 'React / Vite Dashboard', '↓', 'Insights']
                    insert_single_col_table(paras[idx], arch_steps)
                elif line == '[INSERT_FLOW_TABLE]':
                    clear_para(paras[idx])
                    flow_steps = ['START', '↓', 'Load INvideos.csv', '↓', 'Dataset Exploration', '↓', 'Missing / Duplicate Check', '↓', 'Data Cleaning & Formatting', '↓', 'Feature Engineering', '↓', 'Exploratory Data Analysis', '↓', 'Statistical Analysis', '↓', 'Data Visualization', '↓', 'Export CSV', '↓', 'React Dashboard', '↓', 'END']
                    insert_single_col_table(paras[idx], flow_steps)
                else:
                    update_para(paras[idx], line)
        for idx in range(len(lines), len(paras)):
            clear_para(paras[idx])

update_ch8(doc)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 14 – Chapter 9: Conclusion and Future Enhancements
# ─────────────────────────────────────────────────────────────────────────────

def update_ch9(doc):
    ch9_start = find_para_index(doc, 'CHAPTER 9')
    refs_start = find_para_index(doc, 'REFERENCES')
    if ch9_start < 0:
        return
    ch9_paras = doc.paragraphs[ch9_start: refs_start if refs_start > 0 else ch9_start + 80]

    CH9_MAP = {
        '9.1 Conclusion': [
            ('The YouTube Data Analysis System provides an effective approach for '
             'analyzing the India YouTube Trending Videos dataset. The project '
             'demonstrates how data analysis techniques can be applied to real-world '
             'social media data.'),
            ('The project uses data preprocessing, exploratory data analysis, '
             'statistical techniques, and visualization to transform the raw '
             'INvideos.csv dataset into meaningful insights.'),
            ('The system analyzes YouTube channel performance, category distribution, '
             'video views, likes, comments, engagement, engagement rates, and '
             'publishing-time patterns across 33,089 cleaned records.'),
            ('Different visualization techniques such as bar charts, pie charts, '
             'histograms, line charts, and scatter plots are used to represent the '
             'analytical findings clearly.'),
            ('The processed dataset is connected to an interactive React/Vite dashboard '
             'that allows users to dynamically explore the results using filters, charts, '
             'and performance indicators.'),
            ('Overall, the project demonstrates how data analysis can be used to '
             'identify patterns and relationships in YouTube trending data and to '
             'present these insights through an interactive analytical interface.'),
        ],
        '9.2 Limitations': [
            'The project has the following limitations:',
            ('The analysis depends on the quality and completeness of the '
             'INvideos.csv dataset.'),
            ('The dataset represents historical YouTube trending data from India '
             'and does not represent all YouTube videos.'),
            ('The current project mainly focuses on historical data analysis. '
             'Real-time YouTube data integration is not included.'),
            ('Predictive analysis such as view count prediction or trend forecasting '
             'is not part of the core implementation.'),
            ('The engagement calculation is based only on the available likes and '
             'comment_count fields. Additional engagement signals such as shares '
             'are not present in the dataset.'),
            ('The accuracy of insights depends on the available attributes and '
             'the data records present in the dataset.'),
            ('External factors affecting YouTube video popularity such as platform '
             'algorithm changes are not directly represented in the dataset.'),
        ],
        '9.3 Future Enhancements': [
            'The project can be enhanced in the future by implementing:',
            'Real-time YouTube API integration for live data analysis.',
            'Automated dataset updates.',
            'Advanced predictive analytics for view count and trend forecasting.',
            'Sentiment analysis of video comments if comment text is available.',
            'Anomaly detection to identify unusual trending patterns.',
            'Automated report generation from the dashboard.',
            'More advanced dashboard filters and comparison features.',
            'Detailed category-level analysis with content classification.',
            'Multi-country YouTube trending data comparison.',
            'Integration with YouTube Analytics API for creator-level insights.',
            ('The project specification also identifies real-time integration, '
             'predictive analytics, and automated reporting as potential future '
             'extensions.'),
        ],
    }

    current_section = None
    sec_paras = {}

    for p in ch9_paras:
        t = p.text.strip()
        matched = None
        for key in CH9_MAP:
            if key in t:
                matched = key
                break
        if matched:
            current_section = matched
            sec_paras[matched] = []
        elif current_section and t and not any(h in t for h in ['CHAPTER', 'CONCLUSION']):
            sec_paras[current_section].append(p)

    for key, lines in CH9_MAP.items():
        if key not in sec_paras:
            continue
        paras = sec_paras[key]
        for idx, line in enumerate(lines):
            if idx < len(paras):
                if line == '[INSERT_ARCH_TABLE]':
                    clear_para(paras[idx])
                    arch_steps = ['INvideos.csv', '↓', 'Python / Google Colab', '↓', 'Pandas Data Processing', '↓', 'Data Cleaning', '↓', 'Feature Engineering', '↓', 'Exploratory Data Analysis', '↓', 'Statistical Analysis', '↓', 'Data Visualization', '↓', 'youtube_dashboard_data.csv', '↓', 'React / Vite Dashboard', '↓', 'Insights']
                    insert_single_col_table(paras[idx], arch_steps)
                elif line == '[INSERT_FLOW_TABLE]':
                    clear_para(paras[idx])
                    flow_steps = ['START', '↓', 'Load INvideos.csv', '↓', 'Dataset Exploration', '↓', 'Missing / Duplicate Check', '↓', 'Data Cleaning & Formatting', '↓', 'Feature Engineering', '↓', 'Exploratory Data Analysis', '↓', 'Statistical Analysis', '↓', 'Data Visualization', '↓', 'Export CSV', '↓', 'React Dashboard', '↓', 'END']
                    insert_single_col_table(paras[idx], flow_steps)
                else:
                    update_para(paras[idx], line)
        for idx in range(len(lines), len(paras)):
            clear_para(paras[idx])

update_ch9(doc)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 15 – References section
# ─────────────────────────────────────────────────────────────────────────────

def update_references(doc):
    refs_start = find_para_index(doc, 'REFERENCES')
    appendix_start = find_para_index(doc, 'APPENDIX')
    if refs_start < 0:
        return
    ref_paras = doc.paragraphs[refs_start + 1: appendix_start if appendix_start > 0 else refs_start + 20]

    REFS = [
        'Pandas Documentation \u2013 Python Data Analysis Library. https://pandas.pydata.org/docs/',
        'NumPy Documentation \u2013 Numerical Computing with Python. https://numpy.org/doc/',
        'Matplotlib Documentation \u2013 Python Data Visualization. https://matplotlib.org/stable/contents.html',
        'Python Documentation \u2013 Python Programming Language. https://docs.python.org/3/',
        'React Documentation \u2013 JavaScript Library for Building User Interfaces. https://react.dev/',
        'Vite Documentation \u2013 Next Generation Frontend Tooling. https://vitejs.dev/',
        ('PapaParse Documentation \u2013 Fast and Powerful CSV Parsing. '
         'https://www.papaparse.com/docs'),
        ('Recharts Documentation \u2013 Redefined Chart Library Built with React. '
         'https://recharts.org/en-US/'),
        ('YouTube Trending Videos Dataset \u2013 INvideos.csv (India YouTube Trending '
         'Videos Dataset).'),
        ('YouTube Data Analysis System \u2013 Project Specification Document, '
         'DATA ANALYSIS ESSENTIALS, Department of Artificial Intelligence and '
         'Machine Learning, 2026-2027.'),
    ]

    for idx, ref in enumerate(REFS):
        if idx < len(ref_paras):
            update_para(ref_paras[idx], ref)
    for idx in range(len(REFS), len(ref_paras)):
        clear_para(ref_paras[idx])

update_references(doc)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 16 – Appendix: Source Code
# ─────────────────────────────────────────────────────────────────────────────

def update_appendix(doc):
    app_start = find_para_index(doc, 'APPENDIX')
    if app_start < 0:
        return
    update_para(doc.paragraphs[app_start], 'APPENDIX \u2013 SOURCE CODE')
    app_paras = doc.paragraphs[app_start + 1:]

    APPENDIX_SECTIONS = [
        ('A. Import Required Libraries',
         ['import pandas as pd',
          'import matplotlib.pyplot as plt']),

        ('B. Load Dataset',
         ['df = pd.read_csv("INvideos.csv")',
          '',
          'print(df.head())',
          'print(df.shape)']),

        ('C. Dataset Information',
         ['print("Dataset Shape:", df.shape)',
          'print(df.columns.tolist())',
          'print(df.info())',
          'print(df.describe())']),

        ('D. Missing Values',
         ['print(df.isnull().sum())']),

        ('E. Duplicate Records',
         ['print("Duplicate Records:", df.duplicated().sum())',
          '',
          'df = df.drop_duplicates()']),

        ('F. Date and Time Conversion',
         ['# Convert trending_date (format YY.DD.MM)',
          'df["trending_date"] = pd.to_datetime(df["trending_date"], format="%y.%d.%m")',
          '',
          '# Convert publish_time',
          'df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")',
          '',
          '# Extract date/time features',
          'df["publish_year"]  = df["publish_time"].dt.year',
          'df["publish_month"] = df["publish_time"].dt.month_name()',
          'df["publish_day"]   = df["publish_time"].dt.day_name()',
          'df["publish_hour"]  = df["publish_time"].dt.hour']),

        ('G. Engagement Calculation',
         ['df["engagement"] = df["likes"] + df["comment_count"]',
          '',
          'df["engagement_rate"] = (df["engagement"] / df["views"]) * 100']),

        ('H. Select Useful Columns',
         ['youtube_df = df[[',
          '    "video_id", "trending_date", "title", "channel_title",',
          '    "category_id", "publish_time", "views", "likes",',
          '    "dislikes", "comment_count", "publish_year",',
          '    "publish_month", "publish_day", "publish_hour",',
          '    "engagement", "engagement_rate"',
          ']]',
          '',
          'print("Cleaned dataset shape:", youtube_df.shape)']),

        ('I. Channel Analysis',
         ['top_channels = df["channel_title"].value_counts().head(10)',
          '',
          'top_channels.plot(kind="bar")',
          'plt.title("Top 10 Channels by Trending Videos")',
          'plt.xlabel("Channel")',
          'plt.ylabel("Number of Trending Videos")',
          'plt.xticks(rotation=45)',
          'plt.tight_layout()',
          'plt.show()']),

        ('J. Top Videos by Views',
         ['top_videos = df.sort_values("views", ascending=False).head(10)',
          '',
          'top_videos[["title", "channel_title", "views"]].plot(',
          '    x="title", y="views", kind="barh"',
          ')',
          'plt.title("Top 10 Videos by Views")',
          'plt.xlabel("Views")',
          'plt.tight_layout()',
          'plt.show()']),

        ('K. Category Analysis',
         ['category_views = df.groupby("category_id")["views"].sum().sort_values(ascending=False)',
          '',
          'category_views.plot(kind="bar")',
          'plt.title("Category-wise Total Views")',
          'plt.xlabel("Category ID")',
          'plt.ylabel("Total Views")',
          'plt.show()']),

        ('L. Publishing Time Analysis',
         ['# Videos by day',
          'df["publish_day"].value_counts().plot(kind="bar")',
          'plt.title("Videos Published by Day of Week")',
          'plt.xlabel("Day")',
          'plt.ylabel("Count")',
          'plt.show()',
          '',
          '# Videos by hour',
          'df["publish_hour"].value_counts().sort_index().plot(kind="bar")',
          'plt.title("Videos Published by Hour")',
          'plt.xlabel("Hour")',
          'plt.ylabel("Count")',
          'plt.show()']),

        ('M. Views vs Likes Scatter Plot',
         ['plt.scatter(df["views"], df["likes"], alpha=0.3)',
          'plt.title("Views vs Likes")',
          'plt.xlabel("Views")',
          'plt.ylabel("Likes")',
          'plt.show()']),

        ('N. Export Processed Dataset',
         ['youtube_df.to_csv("youtube_dashboard_data.csv", index=False)',
          '',
          'print("Exported:", youtube_df.shape)']),

        ('O. Final Summary',
         ['print("Total Records:", len(youtube_df))',
          'print("Columns:", youtube_df.columns.tolist())',
          '',
          'print("\\nTop KPIs:")',
          'print("Total Views:  ", youtube_df["views"].sum())',
          'print("Total Likes:  ", youtube_df["likes"].sum())',
          'print("Avg Views:    ", youtube_df["views"].mean().round(2))',
          'print("Avg Eng Rate: ", youtube_df["engagement_rate"].mean().round(4), "%")']),
    ]

    flat_lines = []
    for section_title, code_lines in APPENDIX_SECTIONS:
        flat_lines.append(section_title)
        flat_lines.extend(code_lines)
        flat_lines.append('')

    for idx, line in enumerate(flat_lines):
        if idx < len(app_paras):
            update_para(app_paras[idx], line)
    for idx in range(len(flat_lines), len(app_paras)):
        t = app_paras[idx].text.strip()
        if t and 'END OF REPORT' not in t:
            clear_para(app_paras[idx])

update_appendix(doc)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 17 – Final safety pass: remove any remaining old-project keywords
# ─────────────────────────────────────────────────────────────────────────────

FINAL_CLEANUP = [
    ("Employee Attendance and Salary Analysis System",  "YouTube Data Analysis System"),
    ("EMPLOYEE ATTENDANCE AND SALARY ANALYSIS SYSTEM",  "YOUTUBE DATA ANALYSIS SYSTEM"),
    ("employee attendance and salary",                  "YouTube trending video"),
    ("Employee Attendance",                             "YouTube Trending Data"),
    ("employee attendance",                             "YouTube trending data"),
    ("Salary Analysis System",                          "Data Analysis System"),
    ("salary analysis",                                 "engagement analysis"),
    ("Salary analysis",                                 "Engagement analysis"),
    ("payroll",                                         "video engagement"),
    ("Payroll",                                         "Video Engagement"),
    ("absenteeism",                                     "low-engagement patterns"),
    ("Absenteeism",                                     "Low-Engagement Patterns"),
    ("department-wise",                                 "category-wise"),
    ("Department-wise",                                 "Category-wise"),
    ("seaborn",                                         "matplotlib"),
    ("Seaborn",                                         "Matplotlib"),
    ("Power BI",                                        "React/Vite Dashboard"),
    ("employee_attendance_salary.csv",                  "INvideos.csv"),
    ("employee-related",                                "YouTube-trending-related"),
    ("HR departments",                                  "content analysts"),
    ("HR personnel",                                    "data analysts"),
]
global_replace(doc, FINAL_CLEANUP)

# ─────────────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────────────

import time
final_dst = f'C:\\Users\\TEJESWAR\\Desktop\\YouTube-Data-Analysis\\YouTube_Data_Analysis_System_DAE_Report_Final_{int(time.time())}.docx'
try:
    doc.save(final_dst)
    print(f"SUCCESS: Saved perfected report to {final_dst}")
except PermissionError:
    print(f"FAILED: Could not save to {final_dst}")

try:
    doc.save(DST)
    print(f"SUCCESS: Also updated {DST}")
except PermissionError:
    print(f"NOTE: {DST} is currently open in Word. Final document is saved to {final_dst}")
