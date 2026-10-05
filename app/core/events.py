class ConnectionMonitor:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def is_running(self):
        return self.running

    def get_status(self):
        return self.connection_manager.get_status()
