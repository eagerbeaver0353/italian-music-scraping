from crontab import CronTab

# cron = CronTab(user='Administrator')
cron = CronTab(user=True)

# job = cron.new(command='python .\scrape_spotify_italy_daily.py --one-time')
job = cron.new(command='python .\scrape_youtube_italy.py')
job.setall('* * * * *')
# job.setall('0 0 * * * America/New_York')
cron.write()