from django.shortcuts import render
from urllib.parse import quote
from rest_framework import generics
from .models import Trip
from .serializers import TripSerializer
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

class TripCreateView(generics.CreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


@api_view(['GET'])
def geocode(request):
    address = request.query_params.get('address')
    if not address:
        return Response({'error': 'Address is required'}, status=400)

    api_key = '5b3ce3597851110001cf6248b9f7180e99184d30a540eeb335a220ec' 
    url = f'https://api.openrouteservice.org/geocode/search?api_key={api_key}&text={quote(address)}'

    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        if data and data.get('features') and len(data['features']) > 0:
            location = data['features'][0]
            longitude, latitude = location['geometry']['coordinates']
            return Response({
                'longitude': longitude,
                'latitude': latitude,
                'location': location['properties']['label'] #get the address label
            })
        else:
            return Response({'error': 'Location not found'}, status=404)
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=500)
    except ValueError: # handles json decoding errors.
        return Response({'error': 'Invalid JSON response from OpenRouteService'}, status=500)
    except KeyError: #handles cases where the response does not have the expected keys.
        return Response({'error': 'Unexpected response format from OpenRouteService'}, status=500)
