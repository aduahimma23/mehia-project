from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded, GeocoderServiceError
from .models import DeliveryAddress

# Create your views here.
def home(request):
    return render(request, 'main/index.html')


@login_required
def add_delivery_address(request):
    if request == 'POST':
        street_address = request.POST.get('street_address', '')
        city = request.POST.get('city', '')

        full_address = f"{street_address}, {city},"

        try:
            geolocator = GoogleV3("Google Api")
            location = geolocator.geocode(full_address)

            if location:
                delivery_address, created = DeliveryAddress.objects.get_or_create
                street_address = street_address
                city = city
                defaults = {'latitude': location.latitude, 'lontitude': location.longitude}

                return render(request, 'main/delivery_added_address.html', {'delivery_address': delivery_address})
            
            else:
                return render(request, 'address_geocoding_error.html')
            
        except (GeocoderTimedOut, GeocoderQuotaExceeded, GeocoderServiceError) as ex:
            return render(request, 'main/geocoding_error.html', {'error_message': str(ex)})
    
    return render(request, 'main/add_delivery_address')