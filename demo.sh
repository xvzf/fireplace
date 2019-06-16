#!/bin/bash
#
# This script can be used to demo fireplace by starting up multiple dummy sensors & a server
# tmux has to be installed!!!
#

# Create new demo session
SESSION=fireplace
tmux -2 new-session -d -s $SESSION

# Start central server
tmux send-keys ". ./venv/bin/activate && python entrypoint.py server --host 0.0.0.0 --config '$(pwd)/assets/demo/demo.yaml'" C-m

# Start two dummy sensors in split view
tmux new-window -t $SESSION:1 -n 'Sensors'
tmux split-window -h
tmux select-pane -t 0
tmux send-keys ". ./venv/bin/activate && python entrypoint.py client --name sensor0 --host 0.0.0.0 --port 9000" C-m
tmux select-pane -t 1
tmux send-keys ". ./venv/bin/activate && python entrypoint.py client --name sensor1 --host 0.0.0.0 --port 9001" C-m
tmux send-keys "ssh pi@10.0.0.2 \"source /home/pi/fireplace/venv/bin/activate && cd /home/pi/fireplace && python entrypoint.py client --name raspberrypi --host 0.0.0.0 --port 9000 --server http://10.0.0.3/discovery/\"" C-m

# Dummy for showing incoming alerts
tmux new-window -t $SESSION:2 -n "Alerts"
tmux send-keys ". ./venv/bin/activate && python ./assets/demo/telegram.py" C-m

# Attach to the session
tmux -2 attach-session -t $SESSION
