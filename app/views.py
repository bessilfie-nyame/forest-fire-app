from django.shortcuts import render
from .models import *
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from model.model import AppModel

# app model object
appModel = AppModel()
# load model and preprocessing objects
appModel.load()


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

class DashboardView(ListView): #LoginRequiredMixin
    model = ModelOutput
    template_name = "app/dashboard.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["predictions"] = ModelOutput.objects.all()

        return context
