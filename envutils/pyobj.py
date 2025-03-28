class D:
	def __init__(self, **kwargs):
		self.__dict__ = {}
		for key, value in kwargs.items():
			self.__dict__[key] = value

	def __getattribute__(self, name):
		if name == "__dict__":
			return super().__getattribute__(name)
		return self.__dict__[name]

	def __setattr__(self, name, value):
		if name == "__dict__":
			super().__setattr__(name, value)
		else:
			self.__dict__[name] = value

	def __str__(self):
		return str(self.__dict__)

class ADict:
	def __init__(self, **kwargs):
		self.__dict__ = kwargs

	def __getattribute__(self, name):
		if name == "__dict__":
			return super().__getattribute__(name)
		return self.__dict__[name]

	def __setattr__(self, name, value):
		if name == "__dict__":
			super().__setattr__(name, value)
		else:
			self.__dict__[name] = value

	def __str__(self):
		return str(self.__dict__)