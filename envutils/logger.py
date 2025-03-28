import inspect
from operator import call
import os
try:
	import colorama
except ImportError:
	colorama = None
from datetime import datetime

"""
Errors:
[E0001] | When no Origin is specified.
"""


class Logger:
	def __init__(self, verbose: bool = False, log_file: str = f"{datetime.now().strftime('%Y_%m_%d')}/{datetime.now().strftime('%Y_%m_%d-%H:%M:%S')}.log"):
		self.time_format = "%H:%M:%S"
		self.log_location = "logs/"
		self.level = 0
		self.fill = 4
		self.log_file = log_file
		self.log_latest = f"latest.log"
		if verbose:
			print(f"Logging to {self.log_location + self.log_file} from {os.getcwd()}")

		if colorama: colorama.init(autoreset=True)

		if not os.path.exists(self.log_location):
			os.makedirs(self.log_location)

		if not os.path.exists(self.log_location + f"{datetime.now().strftime('%Y_%m_%d')}"):
			os.makedirs(self.log_location + f"{datetime.now().strftime('%Y_%m_%d')}")

		if not os.path.exists(self.log_location + self.log_file):
			with open(self.log_location + self.log_file, "w") as f:
				f.write("\n")

	def set_log_location(self, location):
		self.log_location = location

	def set_fill(self, fill: str):
		self.fill = fill

	def set_level(self, level):
		if level not in ["INFO", "WARNING", "ERROR", "DEBUG", "SYSTEM"]:
			return
		levels = {
			"INFO": 0,
			"WARNING": 1,
			"ERROR": 2,
			"DEBUG": 3,
			"SYSTEM": 4,
			"0": 0,
			"1": 1,
			"2": 2,
			"3": 3,
			"4": 4
		}
		level = levels[level.upper()]
		self.level = level

	def write_to_log(self, x, end="\n"):
		with open(self.log_location + self.log_file, "a") as f:
			f.write(x + end)
		with open(self.log_location + self.log_latest, "a") as f:
			f.write(x + end)

	def __send_with_level(self, level, x: str, only_log: bool = False, call_line: str="", call_location: str=""):
		x = str(x)
		time = datetime.now().strftime(self.time_format)
		msgc = f"[{time}] " + level + f"[{call_location}:{call_line}] " + x
		if colorama:
			colors = {
				"[INFO]": colorama.Fore.GREEN,
				"[WARNING]": colorama.Fore.YELLOW,
				"[ERROR]": colorama.Fore.RED,
				"[DEBUG]": colorama.Fore.BLUE,
				"[SYSTEM]": colorama.Fore.LIGHTBLACK_EX
			}
			msg = colorama.Style.DIM \
				+ colorama.Fore.LIGHTBLACK_EX \
				+ f"[{time}] " \
				+ colorama.Style.RESET_ALL \
				+ colors[level.upper().strip()] \
				+ level \
				+ colorama.Fore.LIGHTBLACK_EX \
				+ f"[{call_location}:{format(call_line, ' ' + str(self.fill))}] " \
				+ colorama.Style.RESET_ALL \
				+ x
		else:
			colors = {
				"[INFO]": "",
				"[WARNING]": "",
				"[ERROR]": "",
				"[DEBUG]": "",
				"[SYSTEM]": ""
			}
			msg = f"[{time}] " + level + f"[{call_location}:{format(call_line, '>' + str(self.fill))}] " + x
		self.write_to_log(msgc)
		if not only_log:
			levels = {
				"[INFO]": 0,
				"[WARNING]": 1,
				"[ERROR]": 2,
				"[DEBUG]": 3,
				"[SYSTEM]": 4
			}
			if self.level >= levels[level.upper().strip()]:
				print(msg)

	def info(self, x: str, only_log: bool = False):
		call_line = "0"
		call_location = "unkown"
		insp = inspect.currentframe()
		if insp != None and insp.f_back is not None:
				call_line = str(insp.f_back.f_lineno)
				call_location = insp.f_back.f_code.co_filename.split("/")[-1]
		self.__send_with_level("[INFO]    ", x, only_log, call_line, call_location)

	def warning(self, x: str, only_log: bool = False):
		call_line = "0"
		call_location = "unkown"
		insp = inspect.currentframe()
		if insp != None and insp.f_back is not None:
				call_line = str(insp.f_back.f_lineno)
				call_location = insp.f_back.f_code.co_filename.split("/")[-1]
		self.__send_with_level("[WARNING] ", x, only_log, call_line, call_location)

	def error(self, x: str, only_log: bool = False):
		call_line = "0"
		call_location = "unkown"
		insp = inspect.currentframe()
		if insp != None and insp.f_back is not None:
				call_line = str(insp.f_back.f_lineno)
				call_location = insp.f_back.f_code.co_filename.split("/")[-1]
		self.__send_with_level("[ERROR]   ", x, only_log, call_line, call_location)

	def debug(self, x: str, only_log: bool = False):
		call_line = "0"
		call_location = "unkown"
		insp = inspect.currentframe()
		if insp != None and insp.f_back is not None:
				call_line = str(insp.f_back.f_lineno)
				call_location = insp.f_back.f_code.co_filename.split("/")[-1]
		self.__send_with_level("[DEBUG]   ", x, only_log, call_line, call_location)

	def system(self, x: str, only_log: bool = False):
		call_line = "0"
		call_location = "unkown"
		insp = inspect.currentframe()
		if insp != None and insp.f_back is not None:
				call_line = str(insp.f_back.f_lineno)
				call_location = insp.f_back.f_code.co_filename.split("/")[-1]
		self.__send_with_level("[SYSTEM]  ", x, only_log, call_line, call_location)