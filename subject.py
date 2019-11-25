

class Subject:
    # The list of observers

    def __init__(self):
        self.observers = list()

    def attach(self, obs):
        self.observers.append(obs)

    def detach(self, obs):
        self.observers.remove(obs)

    def notify_observers(self):
        for obs in self.observers:
            obs.notify()
