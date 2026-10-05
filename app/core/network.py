import socket
import psutil


class NetworkService:

    def get_connection_info(self):
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        preferred = [
            "Wi-Fi",
            "Ethernet",
            "WiFi"
        ]

        for name in preferred:
            if name not in interfaces:
                continue

            if name in stats and not stats[name].isup:
                continue

            ip = None

            for address in interfaces[name]:
                if address.family == socket.AF_INET:
                    ip = address.address
                    break

            if ip:
                return {
                    "connected": True,
                    "name": name,
                    "interface": name,
                    "ip": ip
                }

        for name, addresses in interfaces.items():
            if name in stats and not stats[name].isup:
                continue

            ip = None

            for address in addresses:
                if address.family == socket.AF_INET:
                    ip = address.address
                    break

            if ip and not ip.startswith("127."):
                return {
                    "connected": True,
                    "name": name,
                    "interface": name,
                    "ip": ip
                }

        return {
            "connected": False,
            "name": "",
            "interface": "",
            "ip": ""
        }
