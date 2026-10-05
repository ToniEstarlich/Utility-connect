import asyncio

try:
    from winsdk.windows.networking.connectivity import (
        NetworkInformation
    )
    from winsdk.windows.networking.networkoperators import (
        NetworkOperatorTetheringManager,
        NetworkOperatorTetheringAccessPointConfiguration
    )
    WINSDK_AVAILABLE = True
except Exception:
    WINSDK_AVAILABLE = False


class HotspotService:

    def start(self, ssid, password):
        if not WINSDK_AVAILABLE:
            return {
                "success": False,
                "message": (
                    "Windows networking API is not available in this "
                    "Python environment. Install the required winsdk "
                    "package and run Utility WiFi on Windows 10/11."
                )
            }

        try:
            profile = NetworkInformation.get_internet_connection_profile()

            if profile is None:
                return {
                    "success": False,
                    "message": "No active Internet connection was detected."
                }

            manager = (
                NetworkOperatorTetheringManager
                .create_from_connection_profile(profile)
            )

            config = NetworkOperatorTetheringAccessPointConfiguration()
            config.ssid = ssid
            config.passphrase = password

            manager.configure_access_point_async(config).get()

            result = manager.start_tethering_async().get()

            status = str(result.status)

            if "success" in status.lower():
                return {
                    "success": True,
                    "message": "Hotspot started."
                }

            return {
                "success": False,
                "message": f"Windows could not start the hotspot: {status}"
            }

        except Exception as exc:
            return {
                "success": False,
                "message": (
                    "Windows rejected the hotspot request.\n\n"
                    f"Details: {exc}"
                )
            }

    def stop(self):
        if not WINSDK_AVAILABLE:
            return {
                "success": False,
                "message": "Windows networking API is unavailable."
            }

        try:
            profile = NetworkInformation.get_internet_connection_profile()

            if profile is None:
                return {
                    "success": False,
                    "message": "No connection profile found."
                }

            manager = (
                NetworkOperatorTetheringManager
                .create_from_connection_profile(profile)
            )

            manager.stop_tethering_async().get()

            return {
                "success": True,
                "message": "Hotspot stopped."
            }

        except Exception as exc:
            return {
                "success": False,
                "message": str(exc)
            }
