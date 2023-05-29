from datetime import datetime

from chatbot_logger import UserActivity, SessionProd, UserActions


##################
# Utils
##################

def get_user(username):
    sessions = UserActivity.filter(f'c.username == "{username}"')
    if sessions and len(sessions):
        return sessions[0]
    return None

def get_users(query = '', param = None):
    sessions = UserActivity.filter(query)
    sessions = sorted(sessions, key=lambda sess: sess['params'].get('username') or '', reverse=False)
    if param is not None:
        return [session.get(param) or session['params'].get(param) for session in sessions]
    return sessions


def daily_count(unix_time_array):
    import pandas as pd
    # Convert the array to datetime
    datetime_array = pd.to_datetime(unix_time_array, unit='s')

    # Create a pandas Series
    s = pd.Series(1, index=datetime_array)

    # Resample to daily and count
    daily_counts = s.resample('D').count()

    df_daily = pd.DataFrame(daily_counts, columns=['count']).reset_index()
    df_daily.columns = ['date', 'count']

    return df_daily

def hourly_count(unix_time_array):
    import pandas as pd
    # Convert the array to datetime
    datetime_array = pd.to_datetime(unix_time_array, unit='s')

    # Create a pandas Series
    s = pd.Series(1, index=datetime_array)

    # Resample to hourly and count
    hourly_counts = s.resample('H').count()

    df_hourly = pd.DataFrame(hourly_counts, columns=['count']).reset_index()
    df_hourly.columns = ['date', 'count']

    return df_hourly

##################

def overview(username):
    if not username:
        ui.text('Pick a user')
        return

    user = get_user(username)
    if not user:
        ui.text('User not found')
        return

    ui.header('User Activity')
    ui.subheader(f'User "{user["params"].get("username")}"')
    # ui.json(user)

def plot_sessions_count(df):
    import plotly.graph_objects as go

    fig = go.Figure(data=go.Bar(x=df['date'], y=df['count']))
    fig.update_layout(title_text='Count of Sessions', xaxis_title='Date', yaxis_title='Count')

    return fig

def user_sessions(username):
    user = get_user(username)
    if not user:
        return

    ui.subheader('User Activity')
    all_user_sessions = SessionProd.filter(f'c.username == "{username}"')
    ui.text(f'User sessions count: {len(all_user_sessions)}')

    # ui.json(all_user_sessions)
    timestamps = [session['params'].get('started') or 0 for session in all_user_sessions]
    if not timestamps:
        return

    ui.text('Breakdown by:')
    breakdown_type = ui.toggle_button(left_value='days', right_value='hours')

    if breakdown_type == 'hours':
        data = hourly_count(timestamps)
    else:
        data = daily_count(timestamps)

    ui.text('Visualize with:')
    vis_tye = ui.toggle_button(left_value='table', right_value='chart')

    if vis_tye == 'table':
        ui.table({
            'date': [int(i.timestamp()) for i in data['date'].tolist()],
            'count': [int(i) for i in data['count'].tolist()],
        }, {
            'date': lambda x: ui.text(datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S") if x is not None else '-'),
        })
    else:
        ui.plotly(plot_sessions_count(data))

##################
# Page
##################

try:
    username = state['analytics.py']['username']
except:
    username = ''

username = ui.select(options=get_users('', 'username'), value=username)

overview(username)
user_sessions(username)
