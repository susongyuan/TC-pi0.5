from pathlib import Path
import sys,os,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'code/src'),str(ROOT/'code/packages/openpi-client/src')]
os.environ.setdefault('JAX_PLATFORMS','cpu')
os.environ.setdefault('TORCH_COMPILE_DISABLE','1')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8*1024**2),b''):h.update(b)
 return h.hexdigest()
def manifest():return json.loads((ROOT/'reproduction/release_manifest.json').read_text())
def check_sources():
 expected=json.loads((ROOT/'reproduction/code_sha256.json').read_text())
 for name,digest in expected.items():
  if sha(ROOT/name)!=digest:raise ValueError('Source changed: '+name)
 return len(expected)
def check_weights(folder):
 for f in manifest()['files']:
  if sha(Path(folder)/f['path'])!=f['sha256']:raise ValueError('Weight asset changed: '+f['path'])
def tokenizer_cache(weights):
 import shutil
 cache=ROOT/'.runtime/openpi-cache';p=cache/'big_vision/paligemma_tokenizer.model';p.parent.mkdir(parents=True,exist_ok=True)
 src=Path(weights)/'common/paligemma_tokenizer.model'
 if not p.exists() or sha(p)!=sha(src):shutil.copyfile(src,p)
 os.environ['OPENPI_DATA_HOME']=str(cache)
