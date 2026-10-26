"""Synthetic RGB/proprio + recorded graph interface smoke test, not a task score."""
from _paths import ROOT
import argparse,json,numpy as np
import websockets.sync.client
from tgr.transport import ReliableClient,decode
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=18817);p.add_argument('--output',default='runs/smoke.json');a=p.parse_args()
def connect():return websockets.sync.client.connect(f'ws://127.0.0.1:{a.port}',max_size=None,compression=None)
with connect() as ws:ready=decode(ws.recv(timeout=60))
raw=json.loads((ROOT/'examples/graph_snapshot.json').read_text());session='tcpi-reproducibility-smoke';raw['episode_id']=session
payload={'task':ready['prompt'],'images':{k:np.zeros((3,size,size),np.uint8) for k,size in [('head_rgb',720),('left_wrist_rgb',480),('right_wrist_rgb',480)]},'state':{k:np.zeros(n,np.float32) for k,n in [('base_qvel',3),('trunk_qpos',4),('left_arm',7),('right_arm',7),('left_gripper',2),('right_gripper',2)]},'embodiment_type':'behavior_r1pro','frequency':30.,'graph_snapshot':raw,'sim_time':0.}
client=ReliableClient(connect,ready['weight_sha256'],seed=42);client.session=session
reply=client.request(payload)
result={'status':'passed','scope':'synthetic interface smoke only; not task evaluation','graph_checkpoint_sha256':ready['graph_checkpoint_sha256'],'identity':ready['weight_sha256'],'timing':client.last_timing,'action_groups':{k:np.asarray(v).tolist() for k,v in reply['action'].items()}}
for v in reply['action'].values():assert np.isfinite(np.asarray(v)).all()
from pathlib import Path
out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2));client.close();print(json.dumps(result))
