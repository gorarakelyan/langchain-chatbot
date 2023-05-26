from chatbot_logger import Session, MessagesSequence
from asp import Metric

ui.header("Single Session Details")

try:
    session_hash = state['chatbot/single_session.py']['session_hash']
except:
    session_hash = ''

sessions = Session.filter("")
hashes = [sess['hash'] for sess in sessions]

session_hash = ui.select(options=hashes, value=session_hash)

# History
ui.subheader('Session history')

qa_sequences = MessagesSequence.filter(f's.name == "messages" and c.hash == "{session_hash}"')
qa_sequence = None

if qa_sequences and len(qa_sequences):
    qa_sequence = qa_sequences[0]

if qa_sequence:
    values = qa_sequence['values']
    history_table = ui.table({
        'question': [r['question'] for r in qa_sequence['values']],
        'answer': [r['answer'] for r in qa_sequence['values']],
        'index': [step for (step, _) in enumerate(qa_sequence['values'])],
    })

    if history_table.focused_row:
        ui.subheader('Agent actions')
        step = history_table.focused_row['index']
        ui.json(qa_sequence['values'][step])

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

# User page
ui.subheader('User page')

curr_sess = Session.filter(f'c.hash == "{session_hash}"')
if curr_sess and len(curr_sess):
    curr_sess = curr_sess[0]
    username = curr_sess['params']['username']
    ui.board_link('user_analytics/user_detail.py', 'open user page', state={
        'username': username,
    })
