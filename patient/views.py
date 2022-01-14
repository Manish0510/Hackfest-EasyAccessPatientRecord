from .forms import RegForm, MedicalInfoForm
from django.shortcuts import render,redirect
from .models import PatientProfile

# Create your views here.
def pat_homepage(request):
    patient_id = request.session.get('patient_id')
    patient = PatientProfile.get_patient_by_id(patient_id)
    return render(request, 'pat_home.html', {'patient': patient})


def pat_register(request):
    form = RegForm()
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('login')
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
