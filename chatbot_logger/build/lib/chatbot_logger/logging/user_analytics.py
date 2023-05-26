from aim import Container, Sequence, Object


@Object.alias('aim_qa_logger.UserAction')
class UserAction(Object):
    AIM_NAME = 'aim_qa_logger.UserAction'

    def __init__(self, action_type: str):
        super().__init__()

        self.storage['action_type'] = action_type

    @property
    def action_type(self):
        return self.storage['action_type']


class UserActions(Sequence[UserAction]):
    pass


class UserActivity(Container):
    pass
