"""Install only the exact five upstream Transformer replacement files."""
from _paths import ROOT,sha
import sys,shutil,transformers
from pathlib import Path
assert sys.prefix!=sys.base_prefix,'Use an isolated Python virtual environment'
assert transformers.__version__=='4.53.2',transformers.__version__
src=ROOT/'code/src/openpi/models_pytorch/transformers_replace';dst=Path(transformers.__file__).parent
for f in sorted(src.rglob('*.py')):
 target=dst/f.relative_to(src);target.parent.mkdir(parents=True,exist_ok=True)
 if not target.exists() or sha(target)!=sha(f):shutil.copyfile(f,target)
 assert sha(target)==sha(f)
print('Transformer replacements verified: 5 files')
