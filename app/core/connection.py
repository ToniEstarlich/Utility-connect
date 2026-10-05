class ConnectionManager:
    def __init__(self, network_service, wifi_service, hotspot_service):
        self.network_service = network_service
        self.wifi_service = wifi_service
        self.hotspot_service = hotspot_service

    def detect_source(self):
        return self.network_service.get_active_connection()

    def get_status(self):
        connection = self.detect_source()

        if not connection:
            return "offline"

        return "connected"

    def get_connection_type(self):
        connection = self.detect_source()

        if not connection:
            return None

        return connection.get("interface")

    def check_internet(self):
        return self.network_service.check_internet()

    def start_sharing(self):
        return self.hotspot_service.start()

    def stop_sharing(self):
        return self.hotspot_service.stop()

    def reconnect(self):
        return False

    def monitor(self):
        return self.get_status()
