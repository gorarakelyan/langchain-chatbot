import json
from datetime import datetime
from chatbot_logger import Experiment, SessionDev, Release


##################
# Utils
##################

def get_experiment(session_hash):
    sessions = Experiment.filter(f'c.hash == "{session_hash}"')
    if sessions and len(sessions):
        return sessions[0]
    return None

def get_experiments(query = '', param = None):
    sessions = Experiment.filter(query)
    sessions = sorted(sessions, key=lambda sess: sess['params'].get('started') or 0, reverse=True)
    if param is not None:
        return [session.get(param) for session in sessions]
    return sessions

def get_sessions(query = '', param = None):
    sessions = SessionDev.filter(query)
    sessions = sorted(sessions, key=lambda sess: sess['params'].get('started') or 0, reverse=True)
    if param is not None:
        return [session.get(param) for session in sessions]
    return sessions

def get_releases(query = '', param = None):
    sessions = Release.filter(query)
    sessions = sorted(sessions, key=lambda sess: (sess['params'].get('version') or '0.0.0').split('.'), reverse=True)
    if param is not None:
        return [session.get(param) for session in sessions]
    return sessions

##################

def experiments():
    ui.subheader('Experiments')
    experiments = get_experiments()
    if not experiments or not len(experiments):
        ui.text('No experiments yet')
        return

    table = ui.table({
        'experiment': [sess['hash'] for sess in experiments],
        'version': [sess['params'].get('version') for sess in experiments],
        'time': [sess['params'].get('started') for sess in experiments],
    }, {
        'time': lambda x: ui.text(datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S") if x is not None else '-'),
    })

def sessions_overview():
    sessions = get_sessions()

    if not sessions or not len(sessions):
        return

    ui.subheader('Dev Sessions')

    table = ui.table({
        'session': [sess['hash'] for sess in sessions],
        'experiment': [sess['params'].get('experiment') for sess in sessions],
        'version': [sess['params'].get('chatbot_version') for sess in sessions],
        'model_name': [sess['params'].get('model') for sess in sessions],
        'available_tools': [(str([tool['name'] for tool in sess['params']['available_tools']])) if sess['params'].get('available_tools') else '-' for sess in sessions],
        'time': [sess['params'].get('started') for sess in sessions],
        'type': [sess['type'] for sess in sessions],
    }, {
        'time': lambda x: ui.text(datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S") if x is not None else '-'),
    })

def releases():
    releases = get_releases()

    if not releases or not len(releases):
        ui.text('No releases')
        return

    ui.subheader('Releases')

    table = ui.table({
        'release': [sess['hash'] for sess in releases],
        'version': [sess['params'].get('version') for sess in releases],
        'time': [sess['params'].get('started') for sess in releases],
        'type': [sess['type'] for sess in releases],
    }, {
        'time': lambda x: ui.text(datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S") if x is not None else '-'),
    })

##################
# Page
##################

ui.header('Development')

releases()
experiments()
sessions_overview()
