#!/usr/bin/python
# -*- coding: utf-8 -*-
import calendar

total_lists = 31
list_per_day = 1

year = 2017
month = 1
start_date = 1

weekday_str = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

gaps = []
rev_gaps = [0, 1, 2, 4, 7, 15]

c = calendar.Calendar()
def GetPlannedDayList(year, starting_month):
    planned_days = []
    total_months = 0
    for month_cnt in range(1,12):
        total_months += 1
        for date, weekday in c.itermonthdays2(2017, month_cnt):
            if date == 0:
                continue
            else:
                #if weekday == 0:
                #    weekday = 7
                planned_days.append({'Month': month_cnt, 'Date':date,
                                     'Weekday': weekday, 'Week':weekday_str[weekday], 'New':[], 'Revision':[]})
                for list_number in range(1, min(len(planned_days) + 1, total_lists)):
                    if list_number == len(planned_days):
                        planned_days[-1]['New'].append(list_number)
                    if len(planned_days) - list_number in rev_gaps:
                        planned_days[-1]['Revision'].append(list_number)
                if len(planned_days[-1]['New']) == 0 and len(planned_days[-1]['Revision']) == 0:
                    return planned_days, total_months


def FormatDateInfo(day, newline='\n'):
    temp_str = '%d-%d-%d-%s:' + newline + '\tNew: ' + len(day['New']) * "%d," + newline + '\tRevision: ' + len(day['Revision']) * '%d,' + newline
    pargs = [year, day['Month'], day['Date'], day['Week']]
    pargs.extend(day['New'])
    pargs.extend(day['Revision'])
    return temp_str % tuple(pargs)


def GetTemplateRawData(planned_days):
    text_output = []
    for day in planned_days:
        text_output.append(FormatDateInfo(day))
        #temp_str = '%d-%d-%d-%s:\n\tNew: ' + len(day['New']) * "%d," + '\n\tRevision: ' + len(day['Revision']) * '%d,' + '\n'
        #pargs = [year, day['Month'], day['Date'], day['Week']]
        #pargs.extend(day['New'])
        #pargs.extend(day['Revision'])
        #text_output.append(temp_str % tuple(pargs))

    return text_output


def ClearBlankDatePlaceHolders(line):
    # Clear Blank placeholders
    for i in range(0,8):
        line = line.replace('{$DAY%d}' % i, '')
    return line


def RenderTemplate(raw_data, planned_days, total_months):
    base_template = []
    with open('template', 'r') as f:
        for line in f:
            base_template.append(line)

    table_head = base_template[0:3]
    table_end = base_template[-1]
    line_template = base_template[-2]
    new_line = '<br>'
    output = []

    rendered_days = 0
    real_template = []
    current_month = planned_days[0]['Month']

    real_template.extend(table_head)
    real_template[1] = real_template[1].replace("{$YEAR}", str(2017).encode('utf-8'))
    real_template[1] = real_template[1].replace("{$MONTH}", str(current_month))
    real_template.append(line_template)

    for day in planned_days:
        if day['Month'] != current_month:
            real_template[-1] = ClearBlankDatePlaceHolders(real_template[-1])
            current_month = day['Month']
            real_template.append(table_end)
            real_template.append(new_line)
            real_template.extend(table_head)
            real_template[-2] = real_template[-2].replace('{$MONTH}'.decode('utf-8'), str(current_month))
            real_template[-2] = real_template[-2].replace('{$YEAR}', str(2017))
            real_template.append(line_template)
        elif day['Weekday'] == 0:
            real_template[-1] = ClearBlankDatePlaceHolders(real_template[-1])
            real_template.append(line_template)
        real_template[-1] = real_template[-1].replace('{$DAY%d}' % (day['Weekday'] + 1), FormatDateInfo(day, '<br>'))
    real_template[-1] = ClearBlankDatePlaceHolders(real_template[-1])
    real_template.append(table_end)

    return real_template

if __name__ == "__main__":
    planned_days, total_months = GetPlannedDayList(2017, 1)
    html_output = RenderTemplate(None, planned_days, total_months)
    with open('cal.html', 'w') as f:
        for line in html_output:
            f.write(line)

    txt_output = GetTemplateRawData(planned_days)
    with open('cal.txt', 'w') as f:
        for line in txt_output:
            f.write(line)

