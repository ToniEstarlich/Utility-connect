class DeviceService:
    def get_connected_devices(self):
        return []

    def get_device_count(self):
        return len(self.get_connected_devices())

    def get_device(self, device_id):
        return None

    def rename_device(self, device_id, name):
        return False

    def pause_device(self, device_id):
        return False

    def remove_device(self, device_id):
        return False
