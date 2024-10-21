
import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


def index(request):
    appid = 'baa4b71c8f92b88bb68e5b40a9d17e66'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            # Проверка на наличие города в базе данных
            if not City.objects.filter(name=city_name).exists():
                form.save()

    form = CityForm()
    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()  # Исправил 'cities' на 'city.name'
        print(res)
        if 'main' in res and 'weather' in res:
            city_info = {
                'city': city.name,
                'temp': res['main'].get('temp', 'Неизвестная температура'),
                'icon': res['weather'][0].get('icon', 'нет иконки'),
            }

        else:
            city_info = {
                'city': city.name,
                'error': 'Не удалось получить данные о погоде',
            }

        all_cities.append(city_info)
        print("Вы ввели неправильный Город! Убедитесь в правильности написания Города")


    context = {
        'all_info': all_cities,
        'form': form
    }

    return render(request, 'weather/index.html', context)
