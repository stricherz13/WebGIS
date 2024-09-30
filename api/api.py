from ninja import NinjaAPI
from pydantic import BaseModel
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

api = NinjaAPI()


class PointInput(BaseModel):
    lat: float
    lon: float


# Define a new endpoint to calculate the distance between two points
@api.post("/calculate-distance/")
def calculate_distance(request, point1: PointInput, point2: PointInput):
    # Create Point objects from the input data with SRID 4326 (WGS 84)
    p1 = Point(point1.lon, point1.lat, srid=4326)  # Use (lon, lat) format
    p2 = Point(point2.lon, point2.lat, srid=4326)

    # Calculate the distance using the proper SRID for geographic distance
    distance = p1.distance(p2)  # This returns the distance in degrees

    # Use geodetic distance if you want more accuracy for distance on Earth
    from geopy.distance import geodesic

    geodetic_distance_km = geodesic((point1.lat, point1.lon), (point2.lat, point2.lon)).kilometers

    return {
        "distance_meters": geodetic_distance_km * 1000,  # Convert to meters
        "distance_kilometers": geodetic_distance_km,
        "distance_degrees": distance
    }
