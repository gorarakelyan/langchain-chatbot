__aim_boards__ = 'boards'

from chatbot_logger.logging.chat import *
from chatbot_logger.logging.user_analytics import *

__all__ = [
    'Session', 'SessionProd', 'SessionDev',
    'MessagesSequence', 'UserActivity', 'UserActions',
]

__aim_types__ = [
    Session, SessionProd, SessionDev,
    MessagesSequence, UserActivity, UserActions,
]

for aim_type in __aim_types__:
    setattr(aim_type, '__aim_package__', 'chatbot_logger')
