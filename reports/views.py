from django.shortcuts import render, get_object_or_404, redirect
from .models import Pole, Report
from .forms import ReportForm
from django.contrib import messages



# Create your views here.
def home(request):
    poles = Pole.objects.all()

    context = {
        'poles': poles
    }

    return render(request, 'reports/home.html', context)

def pole_detail(request, id):
    pole = get_object_or_404(Pole, id=id)
    reports = Report.objects.filter(pole=pole).order_by('-reported_at')
    form = ReportForm()
    complaint_id = request.session.pop('complaint_id',None)

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)

        if form.is_valid():
            report = form.save(commit = False)
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            if latitude:
                 report.latitude = float(latitude)

            if longitude:
                report.longitude = float(longitude)

            report.pole = pole
            report.save()
            pole.status = report.reported_status
            pole.save()
            request.session['complaint_id'] = (report.complaint_id)
            messages.success( request, f"Complaint Submitted Successfully! Complaint ID: {report.complaint_id}")
            reports = Report.objects.filter(pole = pole).order_by('-reported_at')
            form = ReportForm()
            return redirect('pole_detail', id=pole.id)
        

    context = {
        'pole' : pole,
        'form' : form,
        'reports': reports,
        'complaint_id': complaint_id
    }
    return render(request, 'reports/pole_detail.html', context)

def about(request):
    return render(request, 'reports/about.html')


def track_complaint(request):
    report = None
    if request.method == "POST":
        complaint_id = request.POST.get('complaint_id')
        try:
            report = Report.objects.get(
                complaint_id = complaint_id.upper()
            )

        except Report.DoesNotExist:
            report = None
    context = {
        'report': report
    }
    return render(
        request, 'reports/track_complaint.html', context)
