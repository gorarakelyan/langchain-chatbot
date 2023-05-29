ui.header('ChatBot Logger')

ui.subheader('Production')
ui.board_link('production.py', 'Overview')
ui.board_link('analytics.py', 'User Page')

ui.subheader('Chat')
ui.board_link('sessions.py', 'Individual Session')

ui.subheader('Development')
ui.board_link('development/_main.py', 'Overview')
ui.board_link('development/experiment.py', 'Experiments')
ui.board_link('development/release.py', 'Releases')
