from django.shortcuts import render
from django.views import View
# Create your views here.
class Dashboard(View):
    def get(self,request):
        return render(request,'admin_templates/evara-backend/index.html')
