# import argparse
import sys
import types
from io  import StringIO
from pathlib  import Path

class XMEnv:
	""" Xmas PyEnv
	Env Structure:
		[root]
			.[lib]
			.[scripts]
	"""
	def __init__(self, dest, pyrt):
		self.envdest = dest
		self.envrt = pyrt
	
	def setupEnv(self):
		# abort for non-empty dst
		# substitute %--XM_*% template variable (%--XM_ENVNAME%, %--XM_ENVPATHS%)
		# copy ['pip', 'python', 'python_d', 'pythonw', 'pythonw_d']
		
		# prepare env & rt
		try:
			rt_exe = Path(self.envrt)
			rt_dir = rt_exe.parent
			assert( rt_dir.is_dir() )
		except:
			raise # ValueError('Invalid Python runtime.')
		
		try:
			env_dir = Path(self.envdest)
			assert( not env_dir.is_file() )
		except:
			raise # ValueError('Invalid destination.')
		else:
			if env_dir.is_dir() and len([*env_dir.iterdir()]) > 0:
				raise ValueError('Destination is not empty.')
		
		# copy runtime binaries
		copy_list = {'': ['python', 'python_d', 'pythonw', 'pythonw_d'], 'scripts': ['pip']}
		
		# pack templates
		
		
		return

class ArgvParser:
	def __init__(self):
		return
	
	def parse(self, argv):
		cls = types.SimpleNamespace()
		
		usage = 'setup [--help] dest'
		try:
			cls.dest = argv[0]
		except:
			raise ValueError('Usage: {}'.format(usage))
		
		return cls

def runWithOptions(options):
	parser = ArgvParser()
	arg = parser.parse(options)
	
	env = XMEnv(arg.dest, sys.executable)
	env.setupEnv()

if __name__ == "__main__":
	runWithOptions(sys.argv[1:])