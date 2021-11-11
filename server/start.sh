#!/bin/bash
gunicorn --timeout 1000 -b 0.0.0.0:5000 'app:create_app()'
