import requests
from django.shortcuts import render
from .models import City

def index(request):

    appid = 'baa4b71c8f92b88bb68e5b40a9d17e66'

    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&units=metric&appid=' + appid


    cities = City.objects.all()

    all_cities = []


    for city in cities:
        res = requests.get(url.format(cities)).json()
        if 'main' in res and 'weather' in res:
            city_info = {
                'city': cities.name,
                'temp': res['main'].get('temp', 'Неизвестная температура'),
                'icon': res['weather'][0].get('icon', 'нет иконки'),
            }
        else:
            city_info = {
                'city': cities,
                'error': 'Не удалось получить данные о погоде',
            }


        all_cities.append(city_info)



    context = {

        'all_info': all_cities}



    return render(request, 'weather/index.html', context)
