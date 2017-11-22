
from .models import Metro, Address


class DBManage():

    def __init__(self, data=None):
        if data:
            self.save_json(data)

    def save_json(self, data):
        if not 'items' in data:
            return None

        for item in data['items']:
            address = item.get('address')
            if not address:
                continue

            metro_stations = address.get('metro_stations')
            del address['metro']
            del address['metro_stations']

            _address, _ = Address.objects.get_or_create(id=address['id'], defaults=address)
            print(_address)

            if not metro_stations:
                continue

            for metro_station in metro_stations:
                _metro_station, _ = Metro.objects.get_or_create(station_id=metro_station['station_id'],
                                                                defaults=metro_station)
                print(_metro_station)
                _address.metro_stations.add(_metro_station)
                _address.save()
