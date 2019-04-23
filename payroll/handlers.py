import datetime

from django.db import transaction

from payroll.models import TimeSheet, TimeReport
from payroll.utils import DATE_FORMAT, get_pay_rate


@transaction.atomic
def handle_uploaded_file(f):
    time_sheet = []
    for idx, line in enumerate(f):
        if idx > 0:
            time_info = line.decode('utf-8').rstrip().split(',')
            if time_info[0] == 'report id':
                if TimeReport.objects.filter(report_id=time_info[1]).exists():
                    raise ValueError(f'Time report already exists: {time_info[1]}')
                else:
                    time_report = TimeReport(report_id=time_info[1], identifier=time_info[2],
                                             upload_time=datetime.datetime.now())
                    TimeReport.save(time_report)
            else:
                work_date = datetime.datetime.strptime(time_info[0], DATE_FORMAT).date()
                if work_date.day <= 15:
                    pay_period = work_date.replace(day=1)
                else:
                    pay_period = work_date.replace(day=16)
                time_record = TimeSheet(date=datetime.datetime.strptime(time_info[0], DATE_FORMAT).date(),
                                        hours=time_info[1], employee_id=time_info[2],
                                        job_group=time_info[3], pay_period=pay_period,
                                        pay_rate=get_pay_rate(time_info[3]))
                time_sheet.append(time_record)

    persist_time_sheet(time_sheet)


def persist_time_sheet(time_sheet):
    TimeSheet.objects.bulk_create(time_sheet)
