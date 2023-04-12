# Set up the cron job to fetch the news every morning.

from crontab import CronTab
cron = ConTab(tab = """0 7 * * * poetry run python """
