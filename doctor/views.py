from django.shortcuts import redirect, render
from .models import *
from django.http import HttpResponse
from patient.models import PatientProfile

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')

        doctor = DoctorProfile.get_doctor_by_email(email)

        error_message = None 

        if doctor and (password== doctor.password):
            request.session['doctor_id'] = doctor.doctor_id
            return redirect('homepage')

        else:
            patient = PatientProfile.get_patient_by_email(email)

            if patient and (password == patient.password):
                request.session['patient_id'] = patient.patient_id
                return redirect('pat_homepage')
            else:
                error_message = 'Invalid Email or Password!!'

        return render(request, 'login.html', {'error_message': error_message})

# Website Hompage
def homepage(request):
    return render(request=request, template_name='homepage.html')
    
def doc_homepage(request):
    return render(request=request, template_name='doc_home.html')

def doc_register(request):
    if request.method == 'POST':
        doctor_name = request.POST.get('name')
        email = request.POST.get('email')
        phone_num = request.POST.get('phone')
        department = request.POST.get('department')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1!=password2:
            return redirect('/doctor/register')
        

        department_inst = Department.objects.filter(department_id = department)[0]

        doctor = DoctorProfile(doctor_name=doctor_name, email=email, phone_num=phone_num, department=department_inst, password = password1)

        doctor.save()
        return HttpResponse('doctor is registered')
        
    else:
        departments = Department.objects.all()
        print(departments)
        return render(request, 'doc_register.html', {'departments' : departments})

def doc_prescription(request):
    prescription = DoctorPrescription.objects.filter(prescription_id=1)
    print(prescription)
    print(prescription.prescription_id)
    print('------------')
    medication_orders = Medication_order.objects.filter(prescription_id=prescription.prescription_id)
    print(prescription)
    sendData = {}
    for med_order in medication_orders:
        print(med_order)
        authorization = Authorisation_details.objects.filter(medication_id=med_order.medication_id)
        med_timing = Medication_timing.objects.filter(medication_id=med_order.medication_id)
        repetation = Repetation.objects.filter(medication_id=med_order.medication_id)
        med_safety = Medication_safety.objects.filter(medication_id=med_order.medication_id)
        print(authorization)
        print(med_timing)
        print(repetation)
        print(med_safety)
        print('-----------------------------------')
        sendData = {'auth':authorization, 'med_timing':med_timing, 'repetation':repetation, 'med_safety':med_safety}
        # return render(request, "doc_prescription.html", sendData)

    # docPresc = DoctorPrescription.objects.all()
    # docMedication = Medication_order.objects.all()
    context = {'presc' : prescription}
    return render(request, "doc_prescription.html", context)