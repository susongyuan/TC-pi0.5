import argparse,json
from _paths import ROOT,check_sources,check_weights,manifest,sha
p=argparse.ArgumentParser();p.add_argument('--weights');a=p.parse_args();n=check_sources()
if a.weights:check_weights(a.weights)
print(json.dumps({'source_files_verified':n,'training_pinned_sources':len(manifest()['implementation_source_sha256']),'weights_verified':bool(a.weights),'name':'TC-π0.5'},indent=2))
