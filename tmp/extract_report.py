import re,zlib,base64
p=r"C:\Users\Serg A\Downloads\Telegram Desktop\C3_Final_Quality_Checked_Report.pdf"; b=open(p,'rb').read(); out=[]
for i,m in enumerate(re.finditer(rb'stream\r?\n',b)):
 e=b.find(b'endstream',m.end()); raw=b[m.end():e]; head=b[max(0,m.start()-300):m.start()]
 try:
  d=raw
  if b'/ASCII85Decode' in head: d=base64.a85decode(d,adobe=True)
  if b'/FlateDecode' in head: d=zlib.decompress(d)
 except: continue
 if b'BT' in d: out.append(f'---STREAM {i}---\n'+d.decode('latin1','ignore'))
open(r'tmp\report_streams.txt','w',encoding='utf8').write('\n'.join(out))
