import json

from chatbot_logger import Session, MessagesSequence
from asp import Metric


##################
# Utils
##################

def get_session(session_hash):
    sessions = Session.filter(f'c.hash == "{session_hash}"')
    if sessions and len(sessions):
        return sessions[0]
    return None

def get_sessions(query = '', param = None):
    sessions = Session.filter(query)
    sessions = sorted(sessions, key=lambda sess: sess['params'].get('started') or 0, reverse=True)
    if param is not None:
        return [session.get(param) for session in sessions]
    return sessions

##################

def overview(session_hash):
    if not session_hash:
        ui.text('Pick a session')
        return

    session = get_session(session_hash)
    if session is None:
        ui.text('Session not found')
        return

    ui.header(f'Session "{session_hash}"')
    ui.subheader('Overview')

    ui.table({
        'Params': [
            'Model',
            'Used tools',
        ],
        'Values': [
            session['params'].get('model'),
            json.dumps(session['params'].get('used_tools')),
        ],
    })

def history(session_hash):
    if not session_hash:
        return

    ui.subheader('Session history')

    qa_sequences = MessagesSequence.filter(f's.name == "messages" and c.hash == "{session_hash}"')
    qa_sequence = None
    if qa_sequences and len(qa_sequences):
        qa_sequence = qa_sequences[0]

    if qa_sequence is not None:
        values = qa_sequence['values']
        history_table = ui.table({
            'question': [r['question'] for r in values],
            'answer': [r['answer'] for r in values],
            'index': [step for (step, _) in enumerate(values)],
        })

        if history_table.focused_row:
            ui.subheader('Agent actions')
            step = history_table.focused_row['index']
            ui.json(values[step])
    else:
        ui.text('No message history')

def session_cost(session_hash):
    if not session_hash:
        return

    ui.subheader('Session tokens usage')

    # Calculate cost
    metrics = Metric.filter(f'c.hash == "{session_hash}"')

    input_tokens = 0
    output_tokens = 0
    for metric in metrics:
        if metric['name'] == 'token-usage-input':
            input_tokens = sum(metric['values'])
        if metric['name'] == 'token-usage-output':
            output_tokens = sum(metric['values'])

    input_price = input_tokens * 0.002 / 1000
    output_price = output_tokens * 0.002 / 1000
    total_price = input_price + output_price

    ui.text(f'Total price: ${total_price}, input tokens: ${input_price}, output tokens: ${output_price}')
    ui.text(f'Total count: {input_tokens+output_tokens}, input count: {input_tokens}, output count: {output_tokens}')

    line_chart = ui.line_chart(metrics, x='steps', y='values')
    line_chart.group('column', ['name'])

def user_info(session_hash):
    if not session_hash:
        return

    session = get_session(session_hash)
    if session is None:
        return

    ui.subheader('Session user')

    username = session['params'].get('username')
    if not username:
        ui.text('No associated user')
        return

    ui.text(f'User: {username}')
    ui.board_link('users/user.py', 'User page', state={
        'username': username,
    })

##################
# Page
##################

try:
    session_hash = state['prod_monitoring/session.py']['session_hash']
except:
    session_hash = ''

session_hash = ui.select(options=get_sessions('', 'hash'), value=session_hash)

overview(session_hash)
history(session_hash)
session_cost(session_hash)
user_info(session_hash)
