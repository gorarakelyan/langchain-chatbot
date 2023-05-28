from datetime import datetime
import json

from chatbot_logger import SessionProd, MessagesSequence


##################
# Utils
##################

def get_sessions(query = '', param = None):
    sessions = SessionProd.filter(query)
    sessions = sorted(sessions, key=lambda sess: sess['params'].get('started') or 0, reverse=True)
    if param is not None:
        return [session.get(param) for session in sessions]
    return sessions

##################

def sessions_overview():
    sessions = get_sessions()

    table = ui.table({
        'session': [sess['hash'] for sess in sessions],
        'version': [sess['params'].get('chatbot_version') for sess in sessions],
        'model_name': [sess['params'].get('model') for sess in sessions],
        'available_tools': [(str([tool['name'] for tool in sess['params']['available_tools']])) if sess['params'].get('available_tools') else '-' for sess in sessions],
        'username': [sess['params'].get('username') for sess in sessions],
        'time': [sess['params'].get('started') for sess in sessions],
        'type': [sess['type'] for sess in sessions],
    }, {
        'username': lambda x: x if x is not None else '-',
        'time': lambda x: ui.text(datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S") if x is not None else '-'),
    })

    if table.focused_row:
        history(table.focused_row['session'])

def history(session_hash):
    if not session_hash:
        return

    ui.subheader(f'Session "{session_hash}"')
    ui.board_link('chat/session.py', 'Open details', state={'session_hash': session_hash})

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
            ui.text('Agent actions:')
            step = history_table.focused_row['index']
            ui.json(values[step])
    else:
        ui.text('No message history')

##################
# Page
##################

ui.header('Production Monitoring')

sessions_overview()
