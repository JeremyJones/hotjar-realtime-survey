sudo nginx 
cd /var/hotjar/dev-task-jeremy
source ./venv/bin/activate
cd app/api
apistar run 2>/dev/null &
