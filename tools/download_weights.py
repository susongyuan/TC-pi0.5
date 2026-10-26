import argparse
from _paths import manifest,check_weights
from huggingface_hub import snapshot_download
p=argparse.ArgumentParser();p.add_argument('--output',default='weights');p.add_argument('--revision');a=p.parse_args();m=manifest()
revision=a.revision or m.get('weights_revision')
if not revision:raise RuntimeError('This source release has no pinned weights revision')
snapshot_download(m['weights_repo'],revision=revision,local_dir=a.output,allow_patterns=[f['path'] for f in m['files']])
check_weights(a.output);print('All weight assets match the tested release')
