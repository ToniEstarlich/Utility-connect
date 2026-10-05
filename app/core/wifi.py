import subprocess
import re


class WiFiService:

    def scan(self):
        try:
            result = subprocess.run(
                ["netsh", "wlan", "show", "networks", "mode=bssid"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore"
            )

            output = result.stdout

            networks = []
            current = None

            for line in output.splitlines():
                stripped = line.strip()

                if stripped.startswith("SSID ") and ":" in stripped:
                    ssid = stripped.split(":", 1)[1].strip()

                    if current:
                        networks.append(current)

                    current = {
                        "ssid": ssid,
                        "signal": 0
                    }

                elif current and "Signal" in stripped and ":" in stripped:
                    value = stripped.split(":", 1)[1].strip()
                    match = re.search(r"(\d+)", value)

                    if match:
                        current["signal"] = int(match.group(1))

            if current:
                networks.append(current)

            unique = {}
            for network in networks:
                unique[network["ssid"]] = network

            return list(unique.values())

        except Exception:
            return []
