from datetime import datetime
from django.core import management

def backup_job():
    print("[{}] Backing up database and media files...".format(datetime.now()))
    management.call_command('dbbackup', '--clean')
    # management.call_command('mediabackup', '--clean')
    print("[{}] Backup done!".format(datetime.now()))