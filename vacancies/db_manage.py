
from .models import Metro, Address
from django.contrib.contenttypes.models import ContentType

import logging

log = logging.getLogger('django')


class DBManage():

    def __init__(self, data=None):
        if data:
            self.save_json(data)

    def get_records_count(self, model=None):
        if model:
            return {model.__name__: model.objects.count()}

        mc = map(lambda x: x.model_class(), ContentType.objects.all())
        mc = filter(lambda x: not x.__module__.startswith('django'), mc)

        return dict(map(lambda x: (x.__name__, x.objects.count()), mc))

    @property
    def records_created(self):
        cb, ca = self.records_before, self.records_after
        return dict(map(lambda k: (k, ca[k] - cb[k]), ca.keys()))

    def save_json(self, data):
        self.records_before = self.get_records_count()
        log.debug(self.records_before)

        self.__save_json(data)

        self.records_after = self.get_records_count()
        log.debug(self.records_after)

        log.info(self.records_created)

    def __save_json(self, data):
        if 'items' not in data:
            return

        for item in data['items']:
            address = item.get('address')
            if not address:
                continue

            metro_stations = address.get('metro_stations')
            del address['metro']
            del address['metro_stations']

            try:
                _address, _ = Address.objects.get_or_create(id=address['id'], defaults=address)
            except Exception as e:
                log.error('Try create address: %s; %s; %s',
                          item.get('id'), address, e.__str__().strip())
                continue

            if not metro_stations:
                continue

            for metro_station in metro_stations:
                try:
                    _metro_station, _ = Metro.objects.get_or_create(station_id=metro_station['station_id'],
                                                                    defaults=metro_station)
                except Exception as e:
                    log.error('Try create metro_station: %s; %s; %s',
                              item.get('id'), metro_station, e.__str__().strip())
                    continue

                _address.metro_stations.add(_metro_station)
