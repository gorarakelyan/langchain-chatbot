from aim import Container, Sequence, Object


@Object.alias('chatbot_logger.Message')
class Message(Object):
    AIM_NAME = 'chatbot_logger.Message'

    def __init__(self, question: str, answer: str, steps: list):
        super().__init__()

        self.storage['question'] = question
        self.storage['answer'] = answer
        self.storage['steps'] = steps

    @property
    def question(self):
        return self.storage['question']

    @property
    def answer(self):
        return self.storage['answer']

    @property
    def steps(self):
        return self.storage['steps']

    def __repr__(self):
        return f'Q: "{self.question}" \n A: "{self.answer}"'


class MessagesSequence(Sequence[Message]):
    pass


class Session(Container):
    pass


class SessionProd(Session):
    pass


class SessionDev(Session):
    pass


class Experiment(Container):
    pass


class Release(Container):
    pass

