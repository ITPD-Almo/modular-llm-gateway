import re,zlib,sys
p=r'C:\Users\Serg A\Downloads\Telegram Desktop\C3_Final_Quality_Checked_Slides.pdf'; b=open(p,'rb').read()
out=[]
for i,m in enumerate(re.finditer(rb'stream\r?\n',b)):
 e=b.find(b'endstream',m.end()); raw=b[m.end():e]
 try:d=zlib.decompress(raw)
 except:d=raw
 if b'BT' in d: out.append(d.decode('latin1','ignore'))
open(r'tmp\streams_text.txt','w',encoding='utf8').write('\n---\n'.join(out))
