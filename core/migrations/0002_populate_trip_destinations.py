from django.db import migrations

def populate_destinations(apps, schema_editor):
    Trip = apps.get_model('core', 'Trip')
    
    # Sensible realistic destinations for trips seeded or created without a destination point
    dest_map = [
        ("Pala KSRTC Bus Station", 9.691200, 76.690400),
        ("St. Thomas Cathedral, Palai", 9.709000, 76.682000),
        ("Lalam Bridge Junction, Palai", 9.708200, 76.683500),
        ("Palai Town Civil Station", 9.710000, 76.680000),
        ("Kottayam Railway Station", 9.591600, 76.522200),
    ]
    
    idx = 0
    trips_to_update = Trip.objects.filter(
        destination_address__isnull=True
    ) | Trip.objects.filter(
        destination_address__in=['', 'Destination Point', 'Destination Drop Point']
    )
    
    for trip in trips_to_update:
        dest_name, lat, lng = dest_map[idx % len(dest_map)]
        trip.destination_address = dest_name
        trip.destination_latitude = lat
        trip.destination_longitude = lng
        trip.end_location = dest_name
        trip.drop_location_name = dest_name
        trip.drop_latitude = lat
        trip.drop_longitude = lng
        trip.save(update_fields=[
            'destination_address', 'destination_latitude', 'destination_longitude',
            'end_location', 'drop_location_name', 'drop_latitude', 'drop_longitude'
        ])
        idx += 1

def reverse_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_destinations, reverse_func),
    ]
