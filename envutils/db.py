from ast import List
import json
from typing import Any

envobj_types = {
	"text": str,
	"int": int,
	"float": float,
	"bool": bool,
	"autoincrement": int,
	"unique": Any
}

class Query:
	def __init__(self, data, full_table):
		self.data = data
		self.full_table = full_table
		self.indices = []

	def where(self, **conditions):
		indices = []
		for col, value in conditions.items():
			suffixes = [
				"__gt",
				"__lt",
				"__gte",
				"__lte",
				"__eq",
				"__ne"
			]
			stripped_col = col
			for suffix in suffixes:
				# key__gt -> key
				stripped_col = stripped_col.removesuffix(suffix)
			if stripped_col not in self.full_table:
				# check if column exists
				raise KeyError(f"Column '{col}' does not exist in the table.")
			# get column values
			column_values = self.full_table[stripped_col]["values"]
			# get matches
			if "__gt" in col:
				col, _ = col.split("__gt")
				matches = [i for i, v in enumerate(column_values) if v > value]
			elif "__lt" in col:
				col, _ = col.split("__lt")
				matches = [i for i, v in enumerate(column_values) if v < value]
			elif "__gte" in col:
				col, _ = col.split("__gte")
				matches = [i for i, v in enumerate(column_values) if v >= value]
			elif "__lte" in col:
				col, _ = col.split("__lte")
				matches = [i for i, v in enumerate(column_values) if v <= value]
			elif "__eq" in col:
				col, _ = col.split("__eq")
				matches = [i for i, v in enumerate(column_values) if v == value]
			elif "__ne" in col:
				col, _ = col.split("__ne")
				matches = [i for i, v in enumerate(column_values) if v != value]
			else:
				matches = [i for i, v in enumerate(column_values) if v == value]
			indices = matches if not indices else list(set(indices) & set(matches))
		# Filter data
		filtered_data = {
			col: {"values": [self.data[col]["values"][i] for i in indices]} for col in self.data
		}
		self.indices = indices  # Save indices for further operations
		return Query(filtered_data, self.full_table)

	def first(self):
		first_row = {}
		for col, col_data in self.data.items():
			first_row[col] = col_data["values"][0] if col_data["values"] else None
		return [first_row]

	def all(self):
		rows = []
		for index in range(len(next(iter(self.data.values()))["values"])):
			row = {}
			for col, col_data in self.data.items():
				row[col] = col_data["values"][index] if col_data["values"] else None
			rows.append(row)
		return rows

class ModifyQuery:
	def __init__(self, full_table):
		self.full_table = full_table
		self.updates = {}
		self.indices = []

	def where(self, **conditions):
		indices = []
		for col, value in conditions.items():
			suffixes = [
				"__gt",
				"__lt",
				"__gte",
				"__lte",
				"__eq",
				"__ne"
			]
			stripped_col = col
			for suffix in suffixes:
				# key__gt -> key
				stripped_col = stripped_col.removesuffix(suffix)
			if stripped_col not in self.full_table:
				# check if column exists
				raise KeyError(f"Column '{col}' does not exist in the table.")
			# get column values
			column_values = self.full_table[stripped_col]["values"]
			# get matches
			if "__gt" in col:
				col, _ = col.split("__gt")
				matches = [i for i, v in enumerate(column_values) if v > value]
			elif "__lt" in col:
				col, _ = col.split("__lt")
				matches = [i for i, v in enumerate(column_values) if v < value]
			elif "__gte" in col:
				col, _ = col.split("__gte")
				matches = [i for i, v in enumerate(column_values) if v >= value]
			elif "__lte" in col:
				col, _ = col.split("__lte")
				matches = [i for i, v in enumerate(column_values) if v <= value]
			elif "__eq" in col:
				col, _ = col.split("__eq")
				matches = [i for i, v in enumerate(column_values) if v == value]
			elif "__ne" in col:
				col, _ = col.split("__ne")
				matches = [i for i, v in enumerate(column_values) if v != value]
			else:
				matches = [i for i, v in enumerate(column_values) if v == value]
			indices = matches if not indices else list(set(indices) & set(matches))

		for index in indices:
			for col, value in self.updates.items():
				self.full_table[col]["values"][index] = value

		return self

	def modify(self, **updates):
		for key, value in updates.items():
			self.updates[key] = value
		return self

class DeleteQuery:
	def __init__(self, full_table):
		self.full_table = full_table
		self.indices = []

	def where(self, **conditions):
		indices = []
		for col, value in conditions.items():
			suffixes = [
				"__gt",
				"__lt",
				"__gte",
				"__lte",
				"__eq",
				"__ne"
			]
			stripped_col = col
			for suffix in suffixes:
				# key__gt -> key
				stripped_col = stripped_col.removesuffix(suffix)
			if stripped_col not in self.full_table:
				# check if column exists
				raise KeyError(f"Column '{col}' does not exist in the table.")
			# get column values
			column_values = self.full_table[stripped_col]["values"]
			# get matches
			if "__gt" in col:
				col, _ = col.split("__gt")
				matches = [i for i, v in enumerate(column_values) if v > value]
			elif "__lt" in col:
				col, _ = col.split("__lt")
				matches = [i for i, v in enumerate(column_values) if v < value]
			elif "__gte" in col:
				col, _ = col.split("__gte")
				matches = [i for i, v in enumerate(column_values) if v >= value]
			elif "__lte" in col:
				col, _ = col.split("__lte")
				matches = [i for i, v in enumerate(column_values) if v <= value]
			elif "__eq" in col:
				col, _ = col.split("__eq")
				matches = [i for i, v in enumerate(column_values) if v == value]
			elif "__ne" in col:
				col, _ = col.split("__ne")
				matches = [i for i, v in enumerate(column_values) if v != value]
			else:
				matches = [i for i, v in enumerate(column_values) if v == value]
			indices = matches if not indices else list(set(indices) & set(matches))

		self.indices = indices
		return self

	def delete(self):
		for index in sorted(self.indices, reverse=True):
			for col in self.full_table:
				del self.full_table[col]["values"][index]

class T:
	def __init__(self, **kwargs: list[str]):
		self.table = {}
		for key, value in kwargs.items():
			self.table[key] = {
				"values": [],
				"types": value if isinstance(value, list) else [value],
			}

	def create(self, **kwargs):
		# Set all columns defined by kwargs
		for key, value in kwargs.items():
			if key in self.table:
				expected_types = self.table[key]["types"]
				if not any(isinstance(value, envobj_types[t]) for t in expected_types):
					raise TypeError(f"Value for '{key}' must be of type(s) {expected_types}.")
				self.table[key]["values"].append(value)
			else:
				raise KeyError(f"Column '{key}' is not defined in the table.")

		# Handle autoincrement for undefined columns in kwargs
		for key, value in self.table.items():
			if key not in kwargs:
				if "autoincrement" in value["types"]:
					current_values = value["values"]
					new_id = (max(current_values) + 1) if current_values else 0
					self.table[key]["values"].append(new_id)
				else:
					self.table[key]["values"].append(None)
		return self

	def _get(self, *args: str):
		# Retrieve specified columns
		cols = {}
		if args[0] != "*":
			cols = {}
			for col in args:
				if col in self.table:
					cols[col] = self.table[col]
				else:
					raise KeyError(f"Column '{col}' does not exist in the table.")
		if len(args) == 1 and args[0] == "*":
			argsn = [col for col in self.table]
			cols = {}
			for col in argsn:
				if col in self.table:
					cols[col] = self.table[col]
				else:
					raise KeyError(f"Column '{col}' does not exist in the table.")
		return cols

	def get(self, *args: str):
		# Prepare a queryable object
		cols = self._get(*args)
		if len(args) == 1 and args[0] == "*":
			argsn = [col for col in self.table]
			cols = self._get(*argsn)
		return Query(cols, self.table)

	def modify(self, **kwargs):
		return ModifyQuery(self.table).modify(**kwargs)

	def delete(self, **kwargs):
		return DeleteQuery(self.table).where(**kwargs).delete()

	def write(self, path: str = "database.db", return_output: bool = False):
		if not return_output:
			with open(path, "wb") as f:
				# clear file
				f.truncate(0)
				# write table
				data = json.dumps(self.table, indent=4).encode("utf-8")
				f.write(data)
		else:
			return json.dumps(self.table, indent=4)
		return self
	def read(self, path: str = "database.db"):
		with open(path, "rb") as f:
			self.table = json.loads(f.read().decode("utf-8"))
		return self

class Database:
	def __init__(self):
		self.tables = {}

	def create(self, name: str, **kwargs):
		self.tables[name] = T(**kwargs)
		return self

	def get(self, name: str):
		return self.tables[name]

	def write(self, path: str = "database.db"):
		outs = List()
		for name, table in self.tables.items():
			out = table.write(path, return_output=True)
			outs.append(out)

		with open(path, "wb") as f:
			# clear file
			f.truncate(0)
			# write tables
			for out in outs:
				data = out
				f.write(data)
		return self