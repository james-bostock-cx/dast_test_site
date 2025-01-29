$env:FLASK_APP = 'dast_test_site.py'
$env:FLASK_DEBUG = 1
$env:FLASK_ENV = 'development'
$env:FLASK_RUN_HOST = '0.0.0.0'
flask run
