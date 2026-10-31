import re,zlib
p=r'C:\Users\Serg A\Downloads\Telegram Desktop\C3_Final_Quality_Checked_Slides.pdf'
b=open(p,'rb').read()
for i,m in enumerate(re.finditer(rb'stream\r?\n',b)):
 e=b.find(b'endstream',m.end()); raw=b[m.end():e]
 try: d=zlib.decompress(raw)
 except: continue
 if b'BT' in d: print('\n---',i,'---\n',d[:10000].decode('latin1','ignore'))
