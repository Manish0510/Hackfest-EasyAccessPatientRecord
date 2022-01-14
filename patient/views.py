from functools import partial
from django.http import HttpResponse
from patient.models import *
from .forms import RegForm, MedicalInfoForm
from django.shortcuts import render,redirect

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

def allpatients(request):
    patients = PatientProfile.objects.all()[0]
    medical_info = MedicalInfo.objects.filter(patient_id=patients.patient_id)
    patient_data = {
        'patients': patients,
        'medical_info':[],
    }
    for data in medical_info:
        print(data.height)
        print(data.weight)
        print(data.bloodType)
        print(data.allergy)
        print(data.medical_history)
        
        medical_info = MedicalInfo.objects.filter(patient_id = data.patient_id)[0]
        print(medical_info)
        medical_info = {
            'medical_info_data':data
        }
        patient_data['medical_info'].append(medical_info)
    print('---------------------')
    print(patients)
    print('---------------------------')
    print(medical_info)
    print('---------------------------')
    print(patient_data)
    print('---------------------------')
    return render(request, 'allpatients.html', patient_data)
    # return HttpResponse('Success')



'''
<QuerySet [<MedicalInfo: aman>]>
aman
---------------------------
<QuerySet [<MedicalInfo: aman>]>
---------------------------
{
    'patients': <PatientProfile: aman>, 
    'medical_info': <QuerySet [<MedicalInfo: aman>]>
}
---------------------------



'''