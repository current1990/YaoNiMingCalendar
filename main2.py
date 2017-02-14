from datetime import date, timedelta
import json

revision_gap = [0, 1, 2, 4, 7, 15]


def get_revision_days(start_date):
    revision_days = []
    for item in revision_gap:
        revision_days.append(start_date + item * timedelta(days=1))
    return revision_days


def generate_full_plan(start_date, total_lists,
                       list_per_day, skip_weekends=False):
    days_for_new_lists = total_lists / list_per_day + 1
    total_days_needed = days_for_new_lists + max(revision_gap)

    one_day_timedelta = timedelta(days=1)

    plan = []

    new_lists = []
    for list_number in range(1, total_lists + 1):
        new_lists.append(list_number)

    # Allocate placeholders for new lists
    for i in range(0, total_days_needed):
        this_day = start_date + i * one_day_timedelta
        plan.append({'year': this_day.year,
                     'month': this_day.month,
                     'day': this_day.day,
                     'new': [],
                     'rev': []})

    # Schdule new lists
    for i in range(len(plan)):
        plan[i]['new'] = new_lists[:list_per_day]
        new_lists = new_lists[list_per_day:]

    # Schdule revisions
    for i in range(len(plan)):
        if(plan[i]['new']):
            for gap in revision_gap:
                plan[i + gap]['rev'].extend(plan[i]['new'])

    return plan

if __name__ == "__main__":
    start_year = int(raw_input('Enter start year:'))
    start_month = int(raw_input('Enter start month:'))
    start_day = int(raw_input('Enter start day:'))
    total_list = int(raw_input('Enter total list count:'))
    list_one_day = int(raw_input('How many new list is scheduled per day:'))
    full_plan = generate_full_plan(date(start_year, start_month, start_day),
                                   total_list, list_one_day)

    for item in full_plan:
        print item

    print json.dumps(full_plan)
