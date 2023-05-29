ui.header('ChatBot Logger')

ui.subheader('Production Monitoring')
ui.board_link('production.py', 'Production Overview')
ui.board_link('analytics.py', 'User Page')

ui.subheader('Development')
ui.board_link('development/_main.py', 'Development Overview')
ui.board_link('development/experiment.py', 'Experiments')
ui.board_link('development/release.py', 'Releases')

ui.subheader('Chat')
ui.board_link('sessions.py', 'Individual Session')