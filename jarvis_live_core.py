import asyncio
import os
import datetime
import threading
from queue import Queue


class JarvisLive:
    def __init__(self):
        self.is_speaking = False
        self.is_paused = False
        self.audio_in_queue = Queue()
        self.lock = threading.Lock()
        self.log_file = "nasa_mission_telemetry.log"

    def log_event(self, subsystem: str, message: str):
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{now_str}] [{subsystem}] {message}"

        print(log_entry)

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")

    def focus_panel(self, panel_name: str, duration_ms: int = 5000):
        self.log_event(
            "JARVIS_UI",
            f"Focusing panel: '{panel_name}' for {duration_ms}ms"
        )

    def interrupt_audio(self):
        try:
            while not self.audio_in_queue.empty():
                self.audio_in_queue.get_nowait()

            self.is_speaking = False
            self.log_event(
                "JARVIS_AUDIO",
                "Audio stream interrupted and cleared."
            )

        except Exception as e:
            self.log_event(
                "JARVIS_ERROR",
                f"Audio interrupt exception: {str(e)}"
            )

    def run_external(self, executable, args=""):
        if not os.path.isfile(executable):
            self.log_event(
                "JARVIS_WARNING",
                f"External subsystem not found: {executable}"
            )
            return

        if not os.access(executable, os.X_OK):
            self.log_event(
                "JARVIS_WARNING",
                f"Subsystem is not executable: {executable}"
            )
            return

        command = f"{executable} {args}".strip()

        self.log_event(
            "JARVIS_ACTION",
            f"Launching subsystem: {command}"
        )

        exit_code = os.system(command)

        self.log_event(
            "JARVIS_ACTION",
            f"Subsystem finished with exit code: {exit_code}"
        )

    async def execute_command(self, query: str):
        query_clean = query.strip().lower()

        self.log_event(
            "JARVIS_CORE",
            f"Executing voice/text command: '{query_clean}'"
        )

        if any(
            w in query_clean
            for w in ["saat", "zaman", "date", "tarih"]
        ):
            self.focus_panel("clock", duration_ms=3200)

            now = datetime.datetime.now().strftime(
                "%H:%M:%S - %d/%m/%Y"
            )

            self.log_event(
                "JARVIS_RESPONSE",
                f"Current system time: {now}"
            )

        elif any(
            w in query_clean
            for w in ["metro", "power", "grid", "ray"]
        ):
            self.focus_panel("power_grid", duration_ms=5000)

            self.log_event(
                "JARVIS_ACTION",
                "Checking Metro Power Subsystem..."
            )

            self.run_external("./metro_power_sim")

        elif any(
            w in query_clean
            for w in ["nasa", "telemetry", "mars", "space"]
        ):
            self.focus_panel(
                "space_telemetry",
                duration_ms=6000
            )

            self.log_event(
                "JARVIS_ACTION",
                "Launching Space Telemetry Engine..."
            )

            self.run_external(
                "./nasa_ultimate_core",
                "MARS 15.0"
            )

        else:
            self.log_event(
                "JARVIS_RESPONSE",
                f"Command '{query_clean}' processed into main queue."
            )


async def main():
    jarvis = JarvisLive()

    jarvis.log_event(
        "JARVIS_SYS",
        "JARVIS Live Autonomous Assist Node Online."
    )

    await jarvis.execute_command(
        "zaman ve saat nedir?"
    )

    await jarvis.execute_command(
        "metro güç durumunu kontrol et"
    )

    await jarvis.execute_command(
        "nasa mars telemetrisini başlat"
    )


if __name__ == "__main__":
    asyncio.run(main())
