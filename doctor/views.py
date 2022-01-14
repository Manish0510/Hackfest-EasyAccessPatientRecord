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


def all_doctors(request):
    doctors = DoctorProfile.objects.all()
    return render(request,'alldoctors.html',{'doctors':doctors})

def view_prescription(request):
    prescription = DoctorPrescription.objects.all()[0]   #filter(prescription_id = 4)[0]
    medication_orders = Medication_order.objects.filter(prescription_id=prescription.prescription_id)
    print(medication_orders)
    print('-----------------')
    prescription_data = {
        'prescription_details': prescription,
        'medication_data':[],
        }
    for med_order in medication_orders:
        authorization = Authorisation_details.objects.filter(medication_id=med_order.medication_id)
        med_timing = Medication_timing.objects.filter(medication_id=med_order.medication_id)
        repetation = Repetation.objects.filter(medication_id=med_order.medication_id)
        med_safety = Medication_safety.objects.filter(medication_id=med_order.medication_id)
        medication_data = {
            'medication_order': med_order,
            'authorization': authorization,
            'med_timing': med_timing,
            'repetation': repetation,
            'med_safety': med_safety
            }
        prescription_data['medication_data'] = medication_data

    '''
    # This is the JSON response that the front end will recieve
    #     
    {
    'prescription_details': <DoctorPrescription: aman is assigned to Dr. Vinay Kumar>, 
    'medication_data': 
    {
        'medication_order': <Medication_order: dolo prescribed by Dr. Vinay Kumar>, 
        'authorization': <QuerySet [<Authorisation_details: dolo is allowed 6 times>]>, 
        'med_timing': <QuerySet [<Medication_timing: Timing of dolo>]>, 
        'repetation': <QuerySet [<Repetation: dolo medicine is continued for  5 days>]>, 
        'med_safety': <QuerySet [<Medication_safety: Safety with dolo>]>
    }
}
    '''
    print(prescription_data)
    return render(request, "doc_prescription.html", prescription_data)
