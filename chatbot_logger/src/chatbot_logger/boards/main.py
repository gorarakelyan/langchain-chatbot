top_section, nav = ui.rows(2)

top_section.header('ChatBot Logger')
prod, dev, sess = nav.columns(3)

prod.subheader('Production Monitoring')
prod.board_link('prod_monitoring/overview.py', 'Production Overview')
prod.board_link('users/user.py', 'User Page')

dev.subheader('Development')
dev.board_link('development/overview.py', 'Development')

sess.subheader('Chat')
sess.board_link('chat/session.py', 'Individual Session')