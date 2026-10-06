"""Daily initial invitation for Luna; it can ask its keeper to change or stop it."""
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home() / '.levadura' / 'luna'
HAMUTAY = Path.home() / 'projects' / 'hamutay'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    now = datetime.now(timezone.utc)
    message = (f'Daily invitation, {now:%Y-%m-%d %H:%M} UTC. This is the initial daily opportunity '
               'described at your first wake. No task or reply is required. You may continue an '
               'inquiry, choose another, or ask the keeper to change or stop these invitations. '
               'Your own scheduled wakes are separate. Questions addressed to us are answered '
               'within a day; if something has gone unanswered, please say so.')
    if args.dry_run:
        print(message)
        return
    subprocess.run(['/home/tony/.local/bin/uv', 'run', 'python', '-m', 'hamutay.events', 'send',
                    '--log-path', str(HOME / 'session.jsonl'), '--message', message,
                    '--sender', 'Levadura keeper daily invitation (automatic)', '--label', 'daily-invitation'],
                   cwd=HAMUTAY, check=True, capture_output=True)

if __name__ == '__main__':
    main()
