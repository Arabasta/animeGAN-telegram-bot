class UserState:
    def __init__(self, default_model="hayao"):
        self.current_model = default_model


class UserStateManager:
    def __init__(self):
        self.user_states = {}

    def get_user_state(self, chat_id: int) -> UserState:
        if chat_id not in self.user_states:
            self.user_states[chat_id] = UserState()
        return self.user_states[chat_id]

    def set_model(self, chat_id: int, model: str):
        self.get_user_state(chat_id).current_model = model