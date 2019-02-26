
#  from importlib import reload  # Python 3.4+ only.

class BetterObjects:


	def __init__(self):
		pass

	def __repr__(self):
		obj_type = type(self).__name__
		print(obj_type + " with properties:\n")

		d = dir(self)
		for i in range(0,len(d)-1):
			if d[i].startswith("__"):
				continue
			if callable(getattr(self,d[i])):
				continue
			print("  " + d[i])

		return ""

	def methods(self):
		"""return a list of methods of this object"""
		m = []
		d = dir(self)
		for i in range(0,len(d)-1):
			if d[i].startswith("__"):
				continue
			if callable(getattr(self,d[i])):
				m.append(d[i])
		return m

	def props(self):
		"""return a list of properties of this object"""
		m = []
		d = dir(self)
		for i in range(0,len(d)-1):
			if d[i].startswith("__"):
				continue
			if callable(getattr(self,d[i])):
				continue
			m.append(d[i])
		return m