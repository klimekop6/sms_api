from time import sleep

from ppadb.client import Client as AdbClient


class AndroidDevice:
    def __init__(self) -> None:
        self.client = AdbClient(host="127.0.0.1", port=5037)
        self.device = self.client.devices()[0]

    def unlock_screen(self) -> None:
        if self.device.shell('dumpsys power | grep "mScreenOn="').rfind("false") != -1:
            self.device.shell("input keyevent 26")  # Wake up

        unlock_swipe = "245 685 245 400"  # x y
        self.device.shell(f"input swipe {unlock_swipe}")  # Swipe up to unlock

    def start_airmore(self) -> None:
        self.device.shell("monkey -p com.airmore -c android.intent.category.LAUNCHER 1")

    def authorize_device(self, wait: float | None = None) -> None:
        if wait:
            sleep(wait)
        self.device.shell("input tap 335 545")


if __name__ == "__main__":
    device = AndroidDevice()
    device.unlock_screen()
    device.start_airmore()
