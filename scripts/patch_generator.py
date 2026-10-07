with open('scripts/generate_report.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update STUDENTS in Table 0 and Table 1
old_table0_block = '''STUDENTS = [
    ("Tejeswar Doolla",    "25B11AIB79"),
    ("Syed Saif Hussain",  "25B11AIB59"),
    ("Lokesh Kapparati",   "25B11AI495"),
    ("Ganusai Vechalapu",  "25B11AIC55"),
]

table0 = doc.tables[0]
# Ensure the table has 4 rows (it may already)
while len(table0.rows) < 4:
    table0.add_row()

for row_idx, (name, sid) in enumerate(STUDENTS):
    row = table0.rows[row_idx]
    # Cell 0: name
    for p in row.cells[0].paragraphs:
        clear_para(p)
        p.add_run(name)
    # Cell 1: ID
    for p in row.cells[1].paragraphs:
        clear_para(p)
        p.add_run(f'({sid})')'''

new_table0_block = '''STUDENTS = [
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
        rn1.bold = True'''

assert old_table0_block in content, 'Table 0 block not found'
content = content.replace(old_table0_block, new_table0_block)

# 2. Update Declaration text block
old_decl_block = '''for p in doc.paragraphs:
    t = p.text.strip()
    if t.startswith('We hereby declare that the project entitled'):
        clear_para(p)
        p.add_run(
            'We hereby declare that the project entitled \u201cYOUTUBE DATA ANALYSIS SYSTEM\u201d '
            'is our original work and is being submitted for the Cornerstone project of B.Tech. '
            'degree in Artificial Intelligence and Machine Learning at KIET Group of Institutions, '
            'Korangi. This project report has not been submitted to any other University or '
            'Institution for the award of any degree or diploma.'
        )
        break

for p in doc.paragraphs:
    if 'Place:Surampalem' in p.text or 'Place: Surampalem' in p.text:
        clear_para(p)
        p.add_run('Place: Surampalem')
    if 'Date:' in p.text and '2026' in p.text:
        clear_para(p)
        p.add_run('Date: 29-09-2026')'''

new_decl_block = '''for p in doc.paragraphs[20:40]:
    t = p.text.strip()
    if t.startswith('We hereby declare that the project entitled'):
        clear_para(p)
        p.add_run(
            'We hereby declare that the project entitled \u201cYOUTUBE DATA ANALYSIS SYSTEM\u201d '
            'is our original work and is submitted to ADITYA UNIVERSITY, Surampalem, in partial '
            'fulfillment of the requirements for the award of the B.Tech. degree in Artificial '
            'Intelligence and Machine learning-'
        )
    if 'Place:Surampalem' in t or 'Place: Surampalem' in t:
        clear_para(p)
        p.add_run('Place:Surampalem\\nDate: 29-09-2026')'''

assert old_decl_block in content, 'Declaration block not found'
content = content.replace(old_decl_block, new_decl_block)

# 3. Replace clear_para on excess paragraphs with delete_paragraph
excess_replacements = [
    ('for idx in range(len(ABSTRACT_LINES), len(abstract_paras)):\n    clear_para(abstract_paras[idx])',
     'for idx in range(len(ABSTRACT_LINES), len(abstract_paras)):\n    delete_paragraph(abstract_paras[idx])'),

    ('for idx in range(len(PROBLEM_LINES), len(problem_list_paras)):\n        clear_para(problem_list_paras[idx])',
     'for idx in range(len(PROBLEM_LINES), len(problem_list_paras)):\n        delete_paragraph(problem_list_paras[idx])'),

    ('for idx in range(len(OBJ_LINES), len(obj_paras)):\n        clear_para(obj_paras[idx])',
     'for idx in range(len(OBJ_LINES), len(obj_paras)):\n        delete_paragraph(obj_paras[idx])'),

    ('for idx in range(len(SCOPE_LINES), len(scope_paras)):\n        clear_para(scope_paras[idx])',
     'for idx in range(len(SCOPE_LINES), len(scope_paras)):\n        delete_paragraph(scope_paras[idx])'),

    ('for idx in range(len(lines), len(paras_to_fill)):\n            clear_para(paras_to_fill[idx])',
     'for idx in range(len(lines), len(paras_to_fill)):\n            delete_paragraph(paras_to_fill[idx])'),

    ('for idx in range(len(lines), len(paras)):\n            clear_para(paras[idx])',
     'for idx in range(len(lines), len(paras)):\n            delete_paragraph(paras[idx])'),

    ('for idx in range(len(REFS), len(ref_paras)):\n        clear_para(ref_paras[idx])',
     'for idx in range(len(REFS), len(ref_paras)):\n        delete_paragraph(ref_paras[idx])'),
]

for old, new in excess_replacements:
    if old in content:
        content = content.replace(old, new)
        print('Replaced excess clearing block successfully.')
    else:
        print('Note: block not found directly, checking variations:', repr(old[:40]))

# 4. Update Table 3 and Table 4
old_table3_block = '''# Update Table 3 (attributes table)
if len(doc.tables) > 3:
    attr_table = doc.tables[3]
    # Clear existing rows except header
    while len(attr_table.rows) > 1:
        tbl = attr_table._tbl
        tbl.remove(attr_table.rows[-1]._tr)

    ATTRS = [
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
        ("publish_year",     "Derived: Year extracted from publish_time"),
        ("publish_month",    "Derived: Month extracted from publish_time"),
        ("publish_day",      "Derived: Day of week extracted from publish_time"),
        ("publish_hour",     "Derived: Hour extracted from publish_time"),
        ("engagement",       "Derived: likes + comment_count"),
        ("engagement_rate",  "Derived: (engagement / views) x 100"),
    ]
    for attr, desc in ATTRS:
        row = attr_table.add_row()
        row.cells[0].text = attr
        row.cells[1].text = desc'''

new_tables_block = '''# Update Table 3 (Original 10 Attributes) & Table 4 (6 Derived Features)
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
        clear_para(p0)
        p0.add_run(attr)
        p1 = row.cells[1].paragraphs[0]
        clear_para(p1)
        p1.add_run(desc)

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
        clear_para(p0)
        p0.add_run(attr)
        p1 = row.cells[1].paragraphs[0]
        clear_para(p1)
        p1.add_run(desc)'''

assert old_table3_block in content, 'Table 3 block not found'
content = content.replace(old_table3_block, new_tables_block)

# 5. Add final purge before saving
purge_code = '''
# ── FINAL PURGE OF EMPTY BULLETS & CONSECUTIVE BLANK PARAGRAPHS ──
paras_to_remove = []
for p in doc.paragraphs:
    num_pr = bool(p._p.xpath('./w:pPr/w:numPr'))
    if num_pr and not any(c.isalnum() for c in p.text):
        paras_to_remove.append(p)

for p in paras_to_remove:
    delete_paragraph(p)

consecutive_empty = 0
excess_empty = []
for p in doc.paragraphs:
    if not p.text.strip():
        consecutive_empty += 1
        if consecutive_empty > 1:
            excess_empty.append(p)
    else:
        consecutive_empty = 0

for p in excess_empty:
    delete_paragraph(p)

final_dst = r'C:\\Users\\TEJESWAR\\Desktop\\YouTube-Data-Analysis\\YouTube_Data_Analysis_System_DAE_Report_Final.docx'
doc.save(final_dst)
print(f'SUCCESS: Saved perfected report to {final_dst}')

try:
    doc.save(DST)
    print(f'SUCCESS: Also updated {DST}')
except PermissionError:
    print(f'NOTE: {DST} is currently locked (open in Word). Final document saved to {final_dst}')
'''

content = content.replace('doc.save(DST)\nprint(f"Saved: {DST}")', purge_code)

with open('scripts/generate_report.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('generate_report.py patched successfully!')
