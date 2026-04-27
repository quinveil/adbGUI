import customtkinter
import adbutils
from adbutils import adb
from tkinter import filedialog
import io

class App(customtkinter.CTk):
	def __init__(self):
		super().__init__()
		w = "500"
		h = "500"
		self.title("ADB")
		self.geometry(f"{w}x{h}")
		self.grid_columnconfigure(0, weight=1)

		self.btn_connect()
		self.btn_install()
		self.txt = customtkinter.CTkTextbox(self, width=400, corner_radius=0)
		self.txt.grid(row=2, column=0, padx=10, pady=10)

	def btn_connect(self):
		self.btn = customtkinter.CTkButton(self, text="Connect", command=self.connect)
		self.btn.grid(row=0, column=0, padx=10, pady=10)

	def btn_install(self):
		self.btn = customtkinter.CTkButton(self, text="Install", command=self.open_file)
		self.btn.grid(row=1, column=0, padx=10, pady=10)

	def open_file(self):
		path = filedialog.askopenfilename(
			title = "Select File",
			filetypes=(("Android Package", "*.apk"),("All Files", "*.*"))
			)
		self.install_app(path)

	def log(self, msg):
		self.txt.insert("end", str(msg) + "\n")
		self.txt.see("end")
	

	def connect(self):
		adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
		output = adb.connect("192.168.240.112:5555")
		devices = adb.list(extended=True)

		if not devices:
			self.log("No devices")
		else:
			for info in devices:
				self.log(f"Serial : {info.serial}")
				self.log(f"State : {info.state}")
				self.log(f"Transport ID : {info.transport_id}")
				self.log("-"*30)

		return adb.device_list()

	def install_app(self, path):
		try:
			d = adb.device()
			d.install(path)
			self.log(f"Installed : {path}")
		except Exception as e:
			self.log(f"Install Failed : {e}")

	

app = App()
app.mainloop()

