ui.header('ChatBot Logger')

ui.subheader('Production Monitoring')
ui.board_link('prod_monitoring/overview.py', 'Production Overview')
ui.board_link('users/user.py', 'User Page')

ui.subheader('Development')
ui.board_link('development/overview.py', 'Development Overview')
ui.board_link('development/experiment.py', 'Experiments')
ui.board_link('development/release.py', 'Releases')

ui.subheader('Chat')
ui.board_link('chat/session.py', 'Individual Session')