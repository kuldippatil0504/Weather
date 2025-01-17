from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'ujjain'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=a01c14fdfcb72f93ffef1f88db2d7858'
    PARAMS = {'units': 'metric'}

    API_KEY = 'AIzaSyA6MPgBQ0Mdlj1sPUz5Mw0lcCmGHrp8Ckg'
    SEARCH_ENGINE_ID = '339b84b413153431d'

    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    try:
        data = requests.get(city_url).json()
        search_items = data.get("items", [])

        # Check if there are at least 2 items in search_items
        if search_items and len(search_items) > 1:
            image_url = search_items[1]['link']
        else:
            image_url = '/static/default-image.jpg'  # Fallback to a default image

        weather_data = requests.get(url, params=PARAMS).json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url,
        })

    except KeyError:
        exception_occurred = True
        messages.error(request, 'Entered data is not available to API')
        day = datetime.date.today()

        # Use default values in case of an exception
        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'indore',
            'exception_occurred': exception_occurred,
            'image_url': '/static/default-image.jpg'  # Default image
        })
