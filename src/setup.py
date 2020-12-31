# import argparse
import os
import shutil
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
	
	@classmethod
	def _isValidDir(cls, p):
		try:
			return (not p.is_file()) and (not (p.is_dir() and len([*p.iterdir()]) > 0))
		except:
			return False
	
	def setupBinary(self, rt_dir, env_dir):
		copy_list = {'': ['python', 'python_d', 'pythonw', 'pythonw_d'], 'scripts': ['pip']}
		for copy_suf in copy_list:
			copy_files = copy_list[copy_suf]
			
			try:
				copy_dir = rt_dir / copy_suf
				assert( copy_dir.is_dir() )
				
				env_cdir = env_dir / copy_suf
				env_cdir.mkdir(exist_ok=True)
				
				for file in copy_dir.iterdir():
					for matchname in copy_files:
						if file.name.startswith(matchname):
							# print(file.absolute())
							shutil.copy2(file, env_cdir)
							break
				
				# for file in copy_files:
					# print((copy_dir / file))
					# assert( (copy_dir / file).is_file() )
			except:
				raise
	
	def setupEnv(self):
		# abort for non-empty dst
		# substitute %--XM_*% template variable (%--XM_ENVNAME%, %--XM_ENVPATHS%)
		# inject environment path (root, root/scripts)
		# copy ['pip', 'python', 'python_d', 'pythonw', 'pythonw_d']
		
		# prepare env & rt
		try:
			rt_exe = Path(self.envrt)
			rt_dir = rt_exe.parent.resolve()
			assert( rt_dir.is_dir() )
		except:
			raise # ValueError('Invalid Python runtime.')
		
		try:
			env_dir = Path(self.envdest).resolve()
			assert( self._isValidDir(env_dir) )
			
			env_bin = env_dir / 'bin'
			
			
			# assert( not env_dir.is_file() )
		except:
			raise # ValueError('Invalid destination.')
		else:
			# if env_dir.is_dir() and len([*env_dir.iterdir()]) > 0:
				# raise ValueError('Destination is not empty.')
			# else:
				
			env_dir.mkdir(exist_ok=True)
		
		try:
			script_dir = (Path(__file__).parent / 'scripts').resolve()
			assert(script_dir.is_dir())
		except:
			raise
		
		# copy runtime binaries
		self.setupConfig(env_dir)
		self.setupBinary(rt_dir, env_dir)
		
		# pack templates
		
		
		paths = os.environ['path'].split(os.pathsep)
		
		return

class ArgvParser:
	def __init__(self):
		return
	
	def parse(self, argv):
		cls = types.SimpleNamespace()
		
		usage = 'setup [--help] dest'
		try:
			cls.dest = argv[0]
			# Usage help
		except Exception as e:
			print('Parser exit with excecption: {}({}).'.format(type(e).__name__, e), file=sys.stderr)
			print(ValueError('Usage: {}\n'.format(usage)), file=sys.stderr)
			
			return None
		
		return cls

def runWithOptions(options):
	parser = ArgvParser()
	arg = parser.parse(options)
	
	if arg != None:
		env = XMEnv(arg.dest, sys.executable)
		env.setupEnv()

if __name__ == "__main__":
	runWithOptions(sys.argv[1:])