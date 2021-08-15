from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required 

from .models import *
from model.model import AppModel

# app model object
appModel = AppModel()
# load model and preprocessing objects
appModel.load()

def login_view(request):
  context = {
    "login_view": "active"
  }
  if request.method == "POST":
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username,
                        password=password)
    if user is not None:
      login(request, user)

      return redirect("home")
    else:
      return HttpResponse("invalid credentials")
  return render(request, "registration/login.html", context)

def logout_request(request):
  logout(request)
  return redirect("home")

class SignUp(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy("login")
  template_name = "registration/signup.html"

def home(request):
  context = {"result": None}

  if request.method == "POST":
    inputs = {}
    
    inputs['horizontalSpatialCoordinate'] = request.POST["x-coordinate"]
    inputs['verticalSpatialCoordinate'] = request.POST["y-coordinate"]         
    inputs['ffmcIndex'] = request.POST["ffmc"]
    inputs['dmcIndex'] = request.POST["dmc"]
    inputs['dcIndex'] = request.POST["dc"]
    inputs['isi'] = request.POST["isi"]
    inputs['temperature'] = request.POST["temperature"]
    inputs['relativeHumidity'] = request.POST["rh"]
    inputs['wind'] = request.POST["wind"]
    inputs['rain'] = request.POST["rain"]

    input_vals = [float(i) for i in inputs.values()]
   
    input_vals = appModel.preprocess([input_vals])
    area = round(appModel.model.predict(input_vals)[0], 3)
    
    context['result'] = [{'area': area, 'inputs': [inputs]}]

  return render(request, 'app/home.html', context=context)

@login_required
def result(request, prediction):
    context = {"result": None}

    prediction = eval(prediction) # unstringify
    if prediction:
        outputs = prediction[0]
        context['result'] = prediction
        
        inputs = outputs['inputs'][0]
        
        modelInput = ModelInput(**inputs)      
        modelInput.save()
        modelOutput = ModelOutput(area=outputs['area'], 
                                    modelInput=modelInput)
        modelOutput.save()
        print('---#Model Result Saved Successfully---')

    return render(request, 'app/result.html', context) 

class DashboardView(LoginRequiredMixin, ListView): 
    model = ModelOutput
    template_name = "app/dashboard.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["predictions"] = ModelOutput.objects.all()

        return context
