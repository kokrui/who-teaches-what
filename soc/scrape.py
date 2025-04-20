import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

def parse_course_row(row):
    cells = row.find_all('td')

    course_code = cells[0].get_text(strip=True)
    course_title = cells[1].get_text(separator="<br/>").split('<br/>')[0].strip()

    data = [None, None]
    for semester in (1, 2):
        semester_cell = cells[semester + 1].get_text(separator="\n").strip()
        grp_idx = semester_cell.find('Grp')
        profs = semester_cell[:grp_idx].strip().split('\n')        
        
        data[semester - 1] = None if profs[0] == '' else {
            'course_code': course_code,
            'course_title': course_title,
            'semester': semester,
            'professors': profs,
        }
    
    return data

url = 'https://www.comp.nus.edu.sg/cug/soc-sched/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')
rows = table.find_all('tr')[1:]  # skip header

courses = []

for row in rows:
    course_data = parse_course_row(row)
    courses.extend(course_data)


script_dir = Path(__file__).resolve().parent
output_path = script_dir / 'soc.json'

with output_path.open('w') as f:
    json.dump(courses, f, indent=2)
