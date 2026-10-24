# Builds dist/artifact/: the game adapted to a claude.ai Artifact page (no own <html>/<head>/<body>, Google Fonts for the face)
import os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'dist', 'artifact')

def main():
    s = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    head = s[s.index('<head>') + 6:s.index('</head>')]
    body = s[s.index('<body>') + 6:s.index('</body>')]
    head = re.sub(r'<meta charset[^>]*>\s*|<meta name="viewport"[^>]*>\s*|<link rel="preload"[^>]*>\s*', '', head)
    head = head.replace('<style>', '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400..700&display=swap">\n<style>', 1)
    head = head.replace('font-family:Pix,monospace', "font-family:'Pixelify Sans',Pix,monospace")
    head = head.replace(':root{', ':root{color-scheme:dark;', 1)
    # SHARE should hand out the public Artifact link, not the sandboxed frame's address
    body = body.replace("const GAME_URL = '';", "const GAME_URL = 'https://claude.ai/artifact/HtcenXTjhcpAY5RyCQsic9';")
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(head.strip() + '\n' + body.strip() + '\n')
    shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(OUT, 'assets'), dirs_exist_ok=True)
    print(OUT)

if __name__ == '__main__':
    main()
