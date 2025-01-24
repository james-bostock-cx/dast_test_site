#!/bin/bash
export FLASK_APP='dast_test_site.py'
export FLASK_DEBUG=1
export FLASK_ENV='development'
export FLASK_RUN_HOST=0.0.0.0
flask run
