from os import environ

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point= 0.1,
    participation_fee= 2.00,
    num_bots= 12,
    doc= "strategicUncertainty"
    )

SESSION_CONFIGS = [
    dict(
        name='strategicUncertainty',
        display_name="strategicUncertainty",
        app_sequence=[
            'intro', 
            'groupAssignment',
            'riskGame1',
            'publicGoodsGame1',
            'publicGoodsGame2',
            'riskGame2',
            'beautyContest',
            'bret',
            'survey'
            ],
        num_demo_participants=3,
    )
    # ,
    # dict(
    #     name='survey', app_sequence=['survey', 'payment_info'], num_demo_participants=1
    # ),
]

SESSION_FIELDS = ['prolific_completion_url']

PARTICIPANT_FIELDS = ['orderOfApps','treatment','numStage','numGame',
    'playerInSession','identity1','identity2','groupID',
    'groupIDRandom2','groupIDRandom4',
    'num_kleesRandom','klees_guessing_kleeRandom',
    'num_kandinskysRandom','kandinskys_guessing_kleeRandom',
    'num_chagallsRandom','chagalls_guessing_kleeRandom',
    'num_picassosRandom','picassos_guessing_kleeRandom',
    'painterQuiz_payoff','painterQuiz_additionalPayoff',
    'painterQuiz_payoffs','riskGame_payoffs','publicGoodsGame_payoffs',
    'allA_payoffs1','allA_payoffs2',
    'beautyOtherChoice1','beautyOtherChoice2','beautyOtherChoice3',
    'beautyContest_payoffs','bombGame_payoffs',
    'rdmOtherChoice','otherGroupID1','otherGroupID2','otherGroupID3',
    'round_to_pay','reset','input',
    'identity','otherKleesIdentity','otherKandinskysIdentity',
    'otherChagallsIdentity','otherPicassosIdentity',
    'riskGame1OtherChoice1','riskGame1OtherChoice2','riskGame1OtherChoice3',
    'riskGame2OtherChoice1','riskGame2OtherChoice2','riskGame2OtherChoice3',
    'choiceNumForPayoff',
    'PGOtherChoice1','PGOtherChoice2','PGOtherChoice3',
    'finished']

REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False
POINTS_DECIMAL_PLACES = 2
LANGUAGE_CODE = 'en-gb'

ROOMS = [
    dict(
        name='session1',
        display_name='session1',
        participant_label_file='_rooms/session1.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = '{{ secret_key }}'
# don't share this with anybody.
# SECRET_KEY = "v5bq+tm%z-8osne3)lknzyge%p@hi-8&lqp)e#9x0=!lroe2e_"

INSTALLED_APPS = ['otree']

SENTRY_DSN = 'http://406c2b097f3340bca2b45ee7edf1f326:031bfc3a03a34af588ff995aedd0f283@sentry.otree.org/211'
