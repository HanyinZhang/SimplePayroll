import calendar

DATE_FORMAT = '%d/%m/%Y'


def get_last_of_month(date):
    return calendar.monthrange(date.year, date.month)[1]


def get_pay_period_str(date):
    last_day = get_last_of_month(date)
    if date.day <= 15:
        end_date = date.replace(day=15)
    else:
        end_date = date.replace(day=last_day)
    return f'{date.strftime(DATE_FORMAT)} - {end_date.strftime(DATE_FORMAT)}'


def get_pay_rate(job_group):
    if job_group == 'A':
        return 20
    elif job_group == 'B':
        return 30
    else:
        return 0
