@echo off
set url_db="http://localhost:9000/sacred"
set url_app="http://127.0.0.1:8050/"
start cmd /k "conda activate SwitchLEDs & omniboard -m 127.0.0.1:27017:sacred"
start cmd /k "conda activate SwitchLEDs & python plotly_app.py"
start chrome %url_db%
start chrome %url_app%
