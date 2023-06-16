from datetime import datetime
from chatbot_logger import Release, Experiment


##################
# Utils
##################

def get_releases(query = '', param = None):
    sessions = Release.filter(query)
    sessions = sorted(sessions, key=lambda sess: (sess['params'].get('version') or '0.0.0').split('.'), reverse=True)
    if param is not None:
        return [session.get(param) or session['params'].get(param) for session in sessions]
    return sessions

def get_release(release_version):
    sessions = Release.filter(f'c.version == "{release_version}"')
    if sessions and len(sessions):
        return sessions[0]
    return None

def get_last_experiment(release_version):
    experiments = Experiment.filter(f'c.version == "{release_version}"')
    last = None
    for experiment in experiments:
        if last is None or not last['params'].get('started'):
            last = experiment
            continue
        if experiment['params'].get('started') and last['params']['started'] < experiment['params']['started']:
            last = experiment
    return last

##################

def experiment(release_version):
    if not release_version:
        return

    exp = get_last_experiment(release_version)
    if not exp:
        ui.text('No experiment')
        return

    ui.subheader('Experiment')

    overview, memory, llm, tools, agent = ui.tabs(['Overview', 'Memory', 'LLM', 'Tools', 'Agent'])

    overview.json({
        'release': exp['params'].get('release'),
        'version': exp['params'].get('version'),
        'started': datetime.fromtimestamp(exp['params'].get('started')).strftime("%Y-%m-%d %H:%M:%S") if exp['params'].get('started') else '-',
    })

    memory.json(exp['params'].get('memory'))
    llm.json(exp['params'].get('llm'))
    tools.json(exp['params'].get('tools'))
    agent.json(exp['params'].get('agent'))

def release(release_version):
    release = get_release(release_version)
    if not release:
        ui.text('Pick a release')
        return

    ui.subheader('Release')
    ui.json(release)

##################
# Page
##################

try:
    release_version = state['development/release.py']['version']
except:
    release_version = ''

releases = get_releases('', 'version')
default_release = releases.index(release_version) if release_version != '' else 0
release_version = ui.select(options=releases, index=default_release)

release(release_version)
experiment(release_version)
