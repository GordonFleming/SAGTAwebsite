from django_cron import CronJobBase, Schedule
from dbbackup.management.commands.dbbackup import Command as DbBackupCommand

class DatabaseBackupCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # every 1 hour (adjust as needed)

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'yourapp.database_backup_cron_job'  # unique code

    def do(self):
        DbBackupCommand().handle()
