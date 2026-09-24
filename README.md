# Webcam Motion Alarm

Live webcam view that flags motion above a sensitivity threshold, logs
each event, and saves a snapshot with the moving region boxed. A five
second cooldown stops it from spamming snapshots during continuous
movement.

## Setup

    pip install -r requirements.txt
    python main.py

Snapshots land in `./snapshots/` next to `main.py`, named by timestamp.
