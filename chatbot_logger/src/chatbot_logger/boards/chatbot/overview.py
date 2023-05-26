from chatbot_logger import Session, MessagesSequence
import json
from datetime import datetime

ui.header('Chatbot Logger')

sessions = Session.filter("")
sessions = sorted(sessions, key=lambda sess: sess['params'].get('started'), reverse=True)

table = ui.table({
    'session': [sess['hash'] for sess in sessions],
    'username': [sess['params'].get('username') for sess in sessions],
    'time': [sess['params'].get('started') for sess in sessions],
    'type': [sess['type'] for sess in sessions],
}, {
    'username': lambda x: x if x is not None else '-',
    'time': lambda x: ui.text(datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S") if x is not None else '-'),
})

if table.focused_row:
    focused_row = table.focused_row
    ui.subheader(f'Session: {focused_row["session"]}')

    qa_sequences = MessagesSequence.filter(f's.name == "messages" and c.hash == "{focused_row["session"]}"')
    qa_sequence = None

    if qa_sequences and len(qa_sequences):
        qa_sequence = qa_sequences[0]

    if qa_sequence:
        values = qa_sequence['values']
        ui.table({
            'question': [r['question'] for r in qa_sequence['values']],
            'answer': [r['answer'] for r in qa_sequence['values']],
        })

    ui.board_link('chatbot/single_session.py', 'View more details', state={'session_hash': focused_row["session"]})
