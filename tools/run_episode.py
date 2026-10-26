"""One BEHAVIOR episode, using the original evaluated deployment actor."""
from _paths import ROOT
import argparse,json,sys,inspect
import websockets.sync.client
from tgr.transport import decode
p=argparse.ArgumentParser();p.add_argument('--instance',type=int,default=308,choices=range(301,311));p.add_argument('--port',type=int,default=18817);p.add_argument('--output',default='runs/episode');a=p.parse_args()
with websockets.sync.client.connect(f'ws://127.0.0.1:{a.port}',max_size=None,compression=None) as ws:ready=decode(ws.recv(timeout=30))
sys.path.insert(0,str(ROOT/'deployment'))
sys.argv=[str(ROOT/'deployment/eval_client.py'),'--output',a.output,'--port',str(a.port),'--start-index',str(a.instance-301),'--protocol',str(ROOT/'reproduction/protocol.json'),'--baseline',str(ROOT/'reports/data_baseline_reference.json'),'--expected-identity',ready['weight_sha256'],'--oracle-upper-bound']
source=(ROOT/'deployment/eval_client.py').read_text();old='args.start_index, args.start_index + 1 if args.preflight_steps else 10';assert source.count(old)==1
# The only execution-wrapper substitution limits the original ten-instance loop to one.
source=source.replace(old,'args.start_index, args.start_index + 1')
exec(compile(source,str(ROOT/'deployment/eval_client.py'),'exec'),{'__name__':'__main__','__file__':str(ROOT/'deployment/eval_client.py')})
