from datetime import datetime
from chatbot_logger import Experiment


##################
# Utils
##################

def get_experiments(query = '', param = None):
    sessions = Experiment.filter(query)
    sessions = sorted(sessions, key=lambda sess: sess['params'].get('started') or 0, reverse=True)
    if param is not None:
        return [session.get(param) for session in sessions]
    return sessions

def get_experiment(session_hash):
    sessions = Experiment.filter(f'c.hash == "{session_hash}"')
    if sessions and len(sessions):
        return sessions[0]
    return None

##################

def experiment(exp_hash):
    exp = get_experiment(exp_hash)
    if not exp:
        ui.text('Pick an experiment')
        return

    ui.header(f'Experiment "{exp_hash}"')

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

##################
# Page
##################

try:
    exp_hash = state['development/experiment.py']['experiment_hash']
except:
    exp_hash = ''

exp_hash = ui.select(options=get_experiments('', 'hash'), value=exp_hash)

experiment(exp_hash)
