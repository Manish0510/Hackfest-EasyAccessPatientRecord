import http
from http.client import HTTPResponse
from multiprocessing import context
from .forms import RegForm, MedicalInfoForm
from django.shortcuts import render,redirect
from patient.models import MedicalInfo, PatientProfile


# Create your views here.
def pat_homepage(request):
    return render(request=request, template_name='pat_home.html')

def pat_register(request):
    form = RegForm()
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('pat_homepage')
    context = {'form': form}
    return render(request, 'pat_register.html', context)


def pat_medicalForm(request):
    form = MedicalInfoForm()
    if request.method == 'POST':
        form = MedicalInfoForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('pat_homepage')
    context = {'form': form}
    return render(request, 'pat_medicalForm.html', context)


def all_patients(request):
    if request.method=='POST':
        email = request.POST.get('email')
        print(email)
        patient_personal_info = PatientProfile.get_patient_by_email(email)
        print(patient_personal_info)
        patient_id = patient_personal_info.getpatient_id
        print(patient_id)
        patient_medical_info = MedicalInfo.objects.get(patient_id)
        context = {patient_personal_info:patient_personal_info,patient_medical_info:patient_medical_info}
        print(context)
        return render(request,'all_patients.html',{patient_personal_info:patient_personal_info,patient_medical_info:patient_medical_info})
    return HTTPResponse('Page Success')