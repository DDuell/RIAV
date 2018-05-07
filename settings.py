import os

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# OTREE_PRODUCTION just controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if os.environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'otree'
# don't share this with anybody.
SECRET_KEY = 'zzzzzzzzzzzzzzzzzzzzzzzzzzz'

PAGE_FOOTER = ''

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
AUTH_LEVEL = os.environ.get('OTREE_AUTH_LEVEL')

# ACCESS_CODE_FOR_DEFAULT_SESSION:
ACCESS_CODE_FOR_DEFAULT_SESSION = 'my_access_code'

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True
LANGUAGE_CODE = 'en-gb'


INSTALLED_APPS = [
    'otree',
]

if 'SENTRY_DSN' in os.environ:
    INSTALLED_APPS += [
        'raven.contrib.django.raven_compat',
    ]

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            Source code
        </a> for the below games.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Below are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish to create your own variations.
    Click one to learn more and play.
</p>
"""

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.01,
    'participation_fee': 4.00,
    'num_bots': 12,
    'doc': "",
    'group_by_arrival_time': False,
}

SESSION_CONFIGS = [
	{
        'name': 'risky_others',
        'display_name': "Risk preferences of others",
        'num_demo_participants': 4,
        'app_sequence': [
            'groupAssignment2',
            'riskGame'
        ],
    },
]

otree.settings.augment_settings(globals())
