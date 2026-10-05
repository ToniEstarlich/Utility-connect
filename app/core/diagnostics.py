class DiagnosticsService:
    def check_internet(self):
        return False

    def ping(self, host="1.1.1.1"):
        return None

    def measure_latency(self):
        return None

    def measure_packet_loss(self):
        return None

    def measure_download_speed(self):
        return None

    def measure_upload_speed(self):
        return None

    def run_full_diagnostic(self):
        return {
            "internet": self.check_internet(),
            "latency": self.measure_latency(),
            "packet_loss": self.measure_packet_loss(),
            "download": self.measure_download_speed(),
            "upload": self.measure_upload_speed(),
        }
