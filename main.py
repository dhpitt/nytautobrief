# Pull top stories for predetermined sections, collate them into one email message, and send it.

import crontab
import datetime
from nyt_interface import retrieve_and_summarize
from gmail_interface import send_email

message_stub = """Dear David, \nHere's your morning briefing.\n"""

sections = ["politics", "science", "business"]

# Pull top stories in each section
# and coerce them into email form.

for sect in sections:
    summary = retrieve_and_summarize(section=sect, length=7)
    if summary[-1] != ".":
        summary += "."
    message_stub += f"\nIn {sect}:\n{summary}\n"

message_stub += "\n\nThat's all for today. Until tomorrow,\nAutoBrief"

# Date the message for today
todays_date = datetime.date.today()
date_str = f"{todays_date.month}-{todays_date.day}-{todays_date.year}"
subject_str = f"{todays_date.month}/{todays_date.day}: your morning briefing"
message_fname = f"./messages/{date_str}.txt"

# Save it to the messages folder
with open(message_fname, "w+") as f:
    f.write(message_stub)
    f.close()

# Pass message to gmail API and send it out!
send_email(to="david.h.pitt@gmail.com", subject=subject_str, body=message_fname)
