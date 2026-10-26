"""Relocatable entry point; original inference, transforms and NN sources unchanged."""
from _paths import ROOT,check_sources,check_weights,tokenizer_cache,sha
from pathlib import Path
import argparse,json,sys
p=argparse.ArgumentParser();p.add_argument('--weights',default='weights');p.add_argument('--port',type=int,default=18817);p.add_argument('--device',default='cuda:0');p.add_argument('--output',default='runs/server');a=p.parse_args()
weights=Path(a.weights).resolve();check_sources();check_weights(weights);tokenizer_cache(weights)
source=weights/'cook_hot_dogs/step5000';original=json.loads((source/'metadata.json').read_text())
staged=ROOT/'.runtime/checkpoint/step5000';staged.mkdir(parents=True,exist_ok=True)
metadata=json.loads(json.dumps(original));metadata['user_stop_evaluation']['run']=str(staged.parent)
(staged/'metadata.json').write_text(json.dumps(metadata,indent=2))
link=staged/'model.safetensors'
if link.is_symlink():link.unlink()
if link.exists():raise FileExistsError(link)
link.symlink_to(source/'model.safetensors')
(staged/'relocation.json').write_text(json.dumps({'original_metadata_sha256':sha(source/'metadata.json'),'only_relocated_field':'user_stop_evaluation.run','original_value':original['user_stop_evaluation']['run'],'runtime_value':metadata['user_stop_evaluation']['run'],'model_bytes_changed':False},indent=2))
sys.argv=[str(ROOT/'src/tgr/serve.py'),'--checkpoint',str(weights/'pi0.5-behaviour-base'),'--delta',str(staged),'--plan',str(ROOT/'reports/data_plan_vocabulary.json'),'--protocol',str(ROOT/'reproduction/protocol.json'),'--output',str(Path(a.output).resolve()),'--port',str(a.port),'--device',a.device,'--oracle-upper-bound']
from tgr.serve import main
main()
