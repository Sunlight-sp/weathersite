from django.shortcuts import render, redirect
from .models import City
from django.contrib import messages
import requests

# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=847d9ec7ba4ad193623c62df5a42ae43'

    cities = City.objects.all().order_by('-pk')

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        # print(r)
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'iconurl':"http://openweathermap.org/img/w/" + r['weather'][0]['icon'] + ".png"
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data}

    return render(request, 'weather/index.html', context)


def add(request):
    if request.method == 'POST':
        name_ = request.POST.get('title').upper()
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=847d9ec7ba4ad193623c62df5a42ae43'
        city_obj = City(name=name_)
        cities = City.objects.all()
        flag=False
        for city in cities:
            if city.name==name_:
                flag=True
                break
        if flag:
            messages.warning(request,"city already added")
            return redirect('/')
        try:
            r = requests.get(url.format(city_obj)).json()
            temp=r['main']['temp']
        except KeyError:
            messages.info(request, "wrong city name")
        else:
            city_obj.save()
            messages.success(request, "successfully added")
        return redirect('/')
