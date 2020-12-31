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
	
	def setupConfig(self, env_dir, setup_dir):
		cfg = setup_dir / 'pyvenv.cfg'
		assert( cfg.is_file() )
		
		shutil.copy2(cfg, env_dir)
	
	def setupBinary(self, env_dir, rt_dir):
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
	
	def setupScripts(self, env_dir, script_dir):
		paths = os.environ['path']
		for addpaths in (env_dir / 'bin', env_dir / 'bin' / 'scripts'):
			paths = '{}{}{}'.format(addpaths.absolute(), os.pathsep, paths)
		
		XM_ENVNAME = 'xm-{}'.format(self.envdest)
		XM_ENVPATHS = paths
		replace_tokens = {'%--XM_ENVNAME%': XM_ENVNAME, '%--XM_ENVPATHS%': XM_ENVPATHS}
		
		for script in script_dir.iterdir():
			assert( script.is_file() )
			
			newfile = env_dir / (script.name)
			with open(newfile, 'w', encoding='utf-8') as nf, script.open() as sf:
				sfdata = sf.read()
				for tok in replace_tokens:
					sfdata = sfdata.replace(tok, replace_tokens[tok])
				
				nf.write(sfdata)
		
	
	def setupEnv(self):
		# abort for non-empty dst
		# substitute %--XM_*% template variable (%--XM_ENVNAME%, %--XM_ENVPATHS%)
		# inject environment path (root, root/scripts)
		# copy ['pip', 'python', 'python_d', 'pythonw', 'pythonw_d']
		
		# prepare env & rt
		try:
			rt_dir = Path(self.envrt).resolve()
			assert( rt_dir.is_dir() )
		except:
			raise # ValueError('Invalid Python runtime.')
		
		try:
			env_dir = Path(self.envdest).resolve()
			assert( self._isValidDir(env_dir) )
			
			env_bindir = env_dir / 'bin'
		except:
			raise # ValueError('Invalid destination.')
		else:
			env_dir.mkdir(exist_ok=True)
			env_bindir.mkdir()
		
		try:
			setup_dir = (Path(__file__).parent).resolve()
			assert(setup_dir.is_dir())
			
			script_dir = setup_dir / 'xmscripts'
			assert(script_dir.is_dir())
		except:
			raise # ValueError('Corrupted setup scripts.')
		
		# copy runtime binaries
		self.setupConfig(env_dir, setup_dir)
		self.setupBinary(env_bindir, rt_dir)
		
		# pack templates
		self.setupScripts(env_dir, script_dir)
		
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
		env = XMEnv(arg.dest, sys.prefix)
		env.setupEnv()

if __name__ == "__main__":
	runWithOptions(sys.argv[1:])