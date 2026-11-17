import asyncio
import os
import ipaddress
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

# تنظیم رنگ زمینه اپلیکیشن به حالت تیره
Window.clearcolor = (0.1, 0.1, 0.1, 1)

class TurboScannerMobile(BoxLayout):
    def __init__(self, **kwargs):
        super(TurboScannerMobile, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        self.is_scanning = False
        self.stop_event = threading.Event()

        # عنوان
        self.add_widget(Label(
            text="⚡ REAL-TIME TURBO SCANNER",
            font_size=20,
            bold=True,
            size_hint_y=None,
            height=40,
            color=(0, 1, 0.8, 1)
        ))

        # ورودی IP یا CIDR
        self.add_widget(Label(text="Enter IP / CIDR / Range:", size_hint_y=None, height=30))
        self.ip_input = TextInput(
            text="185.143.232.0/24",
            multiline=False,
            size_hint_y=None,
            height=45,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1)
        )
        self.add_widget(self.ip_input)

        # ورودی پورت
        self.add_widget(Label(text="Enter Port (e.g. 1080):", size_hint_y=None, height=30))
        self.port_input = TextInput(
            text="1080",
            multiline=False,
            size_hint_y=None,
            height=45,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1)
        )
        self.add_widget(self.port_input)

        # دکمه شروع / توقف
        self.toggle_btn = Button(
            text="Start Turbo Scan 🚀",
            size_hint_y=None,
            height=55,
            background_color=(0, 0.7, 0.3, 1),
            bold=True
        )
        self.toggle_btn.bind(on_press=self.toggle_scan)
        self.add_widget(self.toggle_btn)

        # برچسب وضعیت زنده
        self.status_label = Label(
            text="Status: Idle",
            size_hint_y=None,
            height=35,
            color=(1, 0.8, 0, 1)
        )
        self.add_widget(self.status_label)

        # باکس لاگ‌ها (قابلیت اسکرول)
        scroll = ScrollView(size_hint=(1, 1))
        self.log_box = Label(
            text="[*] Ready to scan...\n",
            size_hint_y=None,
            halign='left',
            valign='top',
            color=(0.8, 0.8, 0.8, 1)
        )
        self.log_box.bind(texture_size=lambda *args: setattr(self.log_box, 'height', self.log_box.texture_size[1]))
        scroll.add_widget(self.log_box)
        self.add_widget(scroll)

    def log(self, message):
        Clock.schedule_once(lambda dt: self._update_log(message))

    def _update_log(self, message):
        self.log_box.text += message + "\n"

    def update_status(self, text):
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', text))

    def toggle_scan(self, instance):
        if not self.is_scanning:
            self.stop_event.clear()
            self.toggle_btn.text = "Stop Scan 🛑"
            self.toggle_btn.background_color = (0.8, 0.1, 0.1, 1)
            self.is_scanning = True
            threading.Thread(target=self.run_scan, daemon=True).start()
        else:
            self.stop_event.set()
            self.log("[!] Stopping scan...")
            self.toggle_btn.text = "Start Turbo Scan 🚀"
            self.toggle_btn.background_color = (0, 0.7, 0.3, 1)
            self.is_scanning = False

    def run_scan(self):
        try:
            val = self.ip_input.text.strip()
            port = int(self.port_input.text.strip())
            
            try:
                ips = [str(ip) for ip in ipaddress.IPv4Network(val, strict=False)]
            except:
                ips = [val]

            targets = [(ip, port) for ip in ips]
            self.log(f"[+] Total Targets: {len(targets)}")
            
            asyncio.run(self.async_scan_runner(targets))
        except Exception as e:
            self.log(f"[!] Error: {str(e)}")
        
        self.is_scanning = False
        self.update_status("Status: Finished / Stopped")
        Clock.schedule_once(lambda dt: setattr(self.toggle_btn, 'text', "Start Turbo Scan 🚀"))
        Clock.schedule_once(lambda dt: setattr(self.toggle_btn, 'background_color', (0, 0.7, 0.3, 1)))

    async def async_scan_runner(self, targets):
        queue = asyncio.Queue()
        for t in targets:
            queue.put_nowait(t)

        total = len(targets)
        processed = [0]
        start_time = asyncio.get_event_loop().time()
        lock = asyncio.Lock()

        async def worker():
            while not self.stop_event.is_set():
                try:
                    ip, port = queue.get_nowait()
                except asyncio.QueueEmpty:
                    break

                try:
                    reader, writer = await asyncio.wait_for(
                        asyncio.open_connection(ip, port), timeout=1.2
                    )
                    writer.write(b"\x05\x01\x00")
                    await writer.drain()
                    response = await asyncio.wait_for(reader.read(2), timeout=1.2)
                    writer.close()
                    await writer.wait_for_closed()

                    if response and response[0] == 0x05:
                        async with lock:
                            res = f"[+] FOUND: {ip}:{port}"
                            self.log(res)
                except:
                    pass

                processed[0] += 1
                if processed[0] % 20 == 0 or processed[0] == total:
                    elapsed = asyncio.get_event_loop().time() - start_time
                    speed = processed[0] / elapsed if elapsed > 0 else 0
                    self.update_status(f"Progress: {processed[0]}/{total} | {speed:.1f} r/s")

                queue.task_done()

        workers = [asyncio.create_task(worker()) for _ in range(150)] # تعداد ورکرها روی موبایل بهینه‌تر شده
        await asyncio.gather(*workers)

class TurboScannerApp(App):
    def build(self):
        self.title = "Real-Time Turbo Scanner Mobile"
        return TurboScannerMobile()

if __name__ == '__main__':
    TurboScannerApp().run()
