#!/bin/bash
export FLASK_APP='dast_test_site.py'
export FLASK_DEBUG=1
export FLASK_ENV='development'
flask run
