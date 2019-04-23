from django.db.models import Sum, F
from django.http import HttpResponseRedirect
from django.shortcuts import render

from payroll.forms import UploadFileForm
from payroll.handlers import handle_uploaded_file
from payroll.models import TimeSheet
from payroll.utils import get_pay_period_str


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['file'])
                return HttpResponseRedirect('done/')
            except Exception as error:
                if isinstance(error, ValueError):
                    report_id = str(error).split(':')[1].strip()
                    error_message = f'report id: {report_id} already exists'
                else:
                    error_message = error
                return HttpResponseRedirect(f'done/?error={error_message}')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def upload_done(request):
    return render(request, 'upload_done.html', {'error': request.GET.get('error')})


def payroll_report(request):
    data = TimeSheet.objects.values('employee_id', 'pay_period', 'job_group').\
        annotate(amount=Sum(F('hours')*F('pay_rate')))
    report_data = [
        {
            'id': r['employee_id'],
            'period': get_pay_period_str(r['pay_period']),
            'amount': r['amount'],
        }
        for r in data]

    return render(request, 'report.html', {'report': report_data})
