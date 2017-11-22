
from django.conf import settings
from django.core.management.base import BaseCommand

import requests
import json


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
        self.search_vacancies(**options)

    def search_vacancies(self, **options):
        url = 'http://localhost:8000'
#        url = 'http://api.hh.ru/vacancies'

        data = {
            'User-Agent': 'jobfinder',
#            'Authorization': 'Bearer {}'.format(settings.ACCESS_TOKEN),
        }

        params = {
            'text': ' '.join(options.get('name', [''])),
            'area': 1,
            'search_field': 'name',
        }

        r = requests.post(url, params=params, data=data)

        print(options)
        print(r.status_code, r.request.url)

        try:
            with open("response.json", "w") as f:
                json.dump(r.json(), f)
        except Exception as e:
            print('Error while saving json response:', e)

# ?text=Python&search_field=name&area=1&salary=&currency_code=RUR
# curl -k -H 'User-Agent: api-test-agent' 'https://api.hh.ru/vacancies?text=java&area=1&metro=6.8'
# curl -k -H 'Authorization: Bearer NM3ND556E8DAPJ5C38412P6OEPH6EPP2RKUPAE3C0MTTNI399V3VEE5I67I3J2ME' -H 'User-Agent: api-test-agent' https://api.hh.ru/resumes/mine
# Authorization: Bearer NM3ND556E8DAPJ5C38412P6OEPH6EPP2RKUPAE3C0MTTNI399V3VEE5I67I3J2ME
