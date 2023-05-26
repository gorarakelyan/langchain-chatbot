from chatbot_logger import UserActivity, Session

# username = 'JamesThompson'
#
# ui.header(f'User analytics: {username}')
#
# activities = UserActivity.filter(f'c.username == "{username}"')
# if activities and len(activities):
#     user_activity = activities[0]
#     ui.text(user_activity.hash)

# ui.header("Single Session Details")
#
# try:
#     session_hash = state['single_session.py']['session_hash']
# except:
#     session_hash = ''

# users = UserActivity.filter("")
# usernames = [user['params']['username'] for user in users]
# ui.select(usernames)

try:
    username = state['user_analytics/user_detail.py']['username']
except:
    username = ''


users = UserActivity.filter("")
usernames = [user['params']['username'] for user in users]
username = ui.select(usernames, username)

all_sessions = Session.filter(f'c.username == "{username}"')
ui.text(f'User sessions: {len(all_sessions)}')
