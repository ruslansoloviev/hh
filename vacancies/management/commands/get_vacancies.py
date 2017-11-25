
from django.conf import settings
from django.core.management.base import BaseCommand

from vacancies.db_manage import DBManage

import logging
import requests
import json

log = logging.getLogger('django')


class Command(BaseCommand):
    help = """
        HELP
        https://github.com/hhru/api
        https://github.com/hhru/api/blob/master/docs/vacancies.md
        https://github.com/hhru/api/blob/master/docs/errors.md
    """

    def add_arguments(self, parser):
        parser.add_argument('name', nargs='*', type=str, help="Search vacancy on hh by name")

    def handle(self, *args, **options):
        log.info('Search vacancies: %s', options)
        self.search_vacancies(**options)

    def search_vacancies(self, page=0, **options):
        url = 'http://127.0.0.1:8000'
        url = 'http://api.hh.ru/vacancies'

        data = {
            'User-Agent': 'jobfinder',
            'Authorization': 'Bearer {}'.format(settings.ACCESS_TOKEN),
        }

        params = {
            'text': ' '.join(options.get('name', [''])),
            'area': 1,
            'search_field': 'name',
            'per_page': 20,
            'page': page,
        }

        try:
            r = requests.post(url, params=params, data=data)
        except Exception as e:
            log.error('request.post: %s', e)
            return

        log.log([logging.ERROR, logging.INFO][r.status_code == 200],
                'status_code: %d; url: %s', r.status_code, r.request.url)

        try:
            DBManage(r.json())
        except Exception as e:
            log.error('Not json (%s)', e)
            return
        else:
            if page < int(r.json().get('pages', 0)) - 1:
                self.search_vacancies(page=page + 1, **options)
                return

        with open("response.json", "w") as f:
            json.dump(r.json(), f)

# ?text=Python&search_field=name&area=1&salary=&currency_code=RUR
# curl -k -H 'User-Agent: api-test-agent' 'https://api.hh.ru/vacancies?text=java&area=1&metro=6.8'
# curl -k -H 'Authorization: Bearer NM3ND556E8DAPJ5C38412P6OEPH6EPP2RKUPAE3C0MTTNI399V3VEE5I67I3J2ME' -H 'User-Agent: api-test-agent' https://api.hh.ru/resumes/mine
# Authorization: Bearer NM3ND556E8DAPJ5C38412P6OEPH6EPP2RKUPAE3C0MTTNI399V3VEE5I67I3J2ME
