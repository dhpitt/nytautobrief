# Set up the cron job to fetch the news every morning.

from crontab import CronTab

cron = CronTab(tab="""0 7 * * * poetry run python main.py""")
cron.write()
