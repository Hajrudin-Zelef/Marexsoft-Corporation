from PIL import Image
import base64, io

full = Image.open('/tmp/marexsoft-logo-original.png').convert('RGB')
emb = Image.open('/tmp/emblem-original.png').convert('RGBA')  # 512, transparent outside

def save_rgba(im, path):
    im.save(path, 'PNG', optimize=True)

def black_icon(size, path):
    bg = Image.new('RGBA', (size, size), (0, 0, 0, 255))
    e = emb.resize((size, size), Image.LANCZOS)
    bg.alpha_composite(e, (0, 0))
    bg.convert('RGB').save(path, 'PNG', optimize=True)

save_rgba(emb.resize((256, 256), Image.LANCZOS), '/tmp/logo-mark.png')
save_rgba(emb.resize((32, 32), Image.LANCZOS), '/tmp/favicon-32.png')
black_icon(180, '/tmp/apple-touch-icon.png')
black_icon(192, '/tmp/icon-192.png')
black_icon(512, '/tmp/icon-512.png')
full.save('/tmp/logo-original.png', 'PNG', optimize=True)

def b64(path):
    return base64.b64encode(open(path,'rb').read()).decode()

# favicon.svg : exact emblem, 128px, embedded
emb128 = io.BytesIO(); emb.resize((128,128), Image.LANCZOS).save(emb128, 'PNG', optimize=True)
fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128" role="img" aria-label="Marexsoft Corp">'
       '<image width="128" height="128" href="data:image/png;base64,' + base64.b64encode(emb128.getvalue()).decode() + '"/></svg>')
open('/tmp/favicon.svg','w').write(fav)

# logo-full.svg : full original logo (emblem + wordmark), resized 600 wide
f600 = full.copy(); f600.thumbnail((600, 608), Image.LANCZOS)
buf = io.BytesIO(); f600.save(buf, 'PNG', optimize=True)
w,h = f600.size
sv = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="Marexsoft Corp">'
      '<image width="%d" height="%d" href="data:image/png;base64,%s"/></svg>') % (w,h,w,h,w,h,base64.b64encode(buf.getvalue()).decode())
open('/tmp/logo-full.svg','w').write(sv)
print('icons ok', w, h)
