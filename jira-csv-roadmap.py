
from string import Template
import csv
import sys
import calendar
import datetime
from dateutil.relativedelta import *

# Usage:
# $ python jira-csv-roadmap.py PROJ Q4 > proj_2019_q4.html
#
# Note that excel mangles dates automatically, this script relies upon use of the JIRA date format.

project = sys.argv[1]
quarter = sys.argv[2]

jira_url_prefix = "https://jira.localhost/browse/"

input_file = project + "Roadmap.csv"
title = project + " " + quarter + " 2019"


with open('year_template.html', 'r') as file:
    year_template = file.read()

yt = Template(year_template)

data = {}
with open(input_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        data[row['Issue key']] = row

months = {}

date_now = datetime.datetime.now()
this_month = int(date_now.strftime("%m"))
for i in range(0,12):
    month_index = (this_month + i) % 12
    if month_index == 0 :
        month_index = 12
    months[i+1] = calendar.month_name[month_index]



def add_start_month_number_and_length(row_dict):
    month_count = 0
    in_month = False
    start_month = 0
    row_start_date = datetime.datetime.strptime(row_dict['Custom field (Target start)'].split(' ')[0], "%d/%b/%y")
    row_end_date = datetime.datetime.strptime(row_dict['Custom field (Target end)'].split(' ')[0], "%d/%b/%y")
    # Assume we are running in the month to start with
    use_date = datetime.datetime.now() + relativedelta(months=-1)
    for m in range(1, 13):
        use_date = use_date + relativedelta(months=+1)
        if (row_start_date <= use_date and row_end_date >= use_date):
            if in_month == False:
                start_month = m
            in_month = True
            month_count += 1
        else:
            in_month = False
    row_dict['start_month'] = start_month
    row_dict['month_count'] = month_count

    return row_dict

def process_row(row_dict):
    ret_val = "<tr>\n"
    col = 0
    for m in range(1, 13):
      col += 1
      if (col < 13):
          ret_val += "  <td "
          if (row_dict['start_month'] == m):
              ret_val += "class=\"ticketContainer\" "
              if (row_dict['month_count'] > 1):
                  col = col + row_dict['month_count'] -1
                  ret_val += "colspan="
                  ret_val += str(row_dict['month_count'])
              ret_val += ">\n"
              ret_val += "    <p class=\"ticket\">\n"
              ret_val += "     <a href=" + jira_url_prefix + row_dict['Issue key'] + ">"
              ret_val += row_dict['Summary']
              ret_val += " </a>\n"
              ret_val += "    </p>\n"
          else:
              if (col % 2 == 0):
                  ret_val += "class=\"evenRow\" "
              else:
                  ret_val += "class=\"oddRow\" "
              ret_val += ">\n"
          ret_val += "  </td>\n"

    ret_val += "</tr>\n"
    return ret_val

rows = ''
for key in sorted(data.keys()):
    rows += process_row(add_start_month_number_and_length(data[key]))

yd = {"title": title,
     "m1": months[1],
     "m2": months[2],
     "m3": months[3],
     "m4": months[4],
     "m5": months[5],
     "m6": months[6],
     "m7": months[7],
     "m8": months[8],
     "m9": months[9],
     "m10": months[10],
     "m11": months[11],
     "m12": months[12],
     "rows": rows
     }

s = yt.substitute(**yd)
print(s)
