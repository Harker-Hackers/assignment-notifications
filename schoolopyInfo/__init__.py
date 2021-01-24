import schoolopy
from os import getenv
schoolopyAuth = schoolopy.Auth(getenv('SCHOOLOGY_KEY'), getenv('SCHOOLOGY_SECRET'), three_legged=True, domain='https://schoology.harker.org/')
schoolopyUrl = schoolopyAuth.request_authorization().replace('https%3A%2F%2Fschoology.harker.org%2F', 'localhost/')