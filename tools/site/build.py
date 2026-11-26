"""Build both sites from ONE canonical source.
Canonical source: editor_nl.html (the Dutch editor = the Voorspellingschecker artifact page).
Outputs (in --out, default ./out):
  nl_editor.html  -> publish to artifact 874758de-e1ed-4185-9536-a26cdfbf83c4 (Voorspellingschecker)
  en_editor.html  -> publish to artifact f6eaae4e-6999-4370-95c7-0438eca11e86 (Prediction Checker)
  nl_public.html  -> index.html of github.com/voorspellingchk/voorspellingschecker (voorspellingschecker.nl)
  en_public.html  -> index.html of github.com/voorspellingchk/predictionchecker (predictionchk.com)
Usage: python3 build.py [editor_nl.html] [--out DIR]
Every new feature or design change goes into editor_nl.html only. New Dutch text must get an English
translation in en_code.json (exact snippets, longest first) or en_text.json (short phrases inside text);
the build fails if Dutch words are left in the English output."""
import json,os,re,subprocess,sys
D=os.path.dirname(os.path.abspath(__file__))
args=[a for a in sys.argv[1:] if not a.startswith('--')]
src=args[0] if args else os.path.join(D,'editor_nl.html')
out=sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else os.path.join(D,'out')
os.makedirs(out,exist_ok=True)
nl=open(src,encoding='utf-8').read()
open(os.path.join(out,'nl_editor.html'),'w',encoding='utf-8').write(nl)
r=subprocess.run([sys.executable,os.path.join(D,'make_en.py'),src,os.path.join(out,'en_editor.html')],capture_output=True,text=True)
print(r.stdout.strip());print(r.stderr.strip())
if r.returncode: sys.exit(r.returncode)
en=open(os.path.join(out,'en_editor.html'),encoding='utf-8').read()
def public(s,cfg,title=None,meta=''):
    if title: s=s.replace(re.search(r'<title>[^<]*</title>',s).group(0),'<title>'+title+'</title>\n'+meta,1)
    return s.replace('<script>\n{','<script>window.VC_PUBLIC='+json.dumps(cfg)+';</script>\n<script>\n{',1)
NLMETA=('<meta name="description" content="De Voorspellingschecker checkt voorspellingen van bekende Nederlanders, '
 'wetenschappers, politici en instituten: correct, deels correct of niet correct.">\n'
 '<meta property="og:title" content="De Voorspellingschecker">\n'
 '<meta property="og:description" content="Checkt alle voorspellingen. Voorspelling gezien? Stuur een tip.">\n')
ENMETA=('<meta name="description" content="Prediction Checker tracks predictions by scientists, politicians, '
 'commentators and institutions, and checks them: correct, partly correct or wrong.">\n'
 '<meta property="og:title" content="Prediction Checker">\n'
 '<meta property="og:description" content="Checking every prediction. Spotted one? Send a tip.">\n')
open(os.path.join(out,'nl_public.html'),'w',encoding='utf-8').write(public(nl,{'tipUrl':'https://docs.google.com/forms/d/e/1FAIpQLScsHrmij3OBocbzei1y7ayw-ZAqygWyX8HMBcVAxEtMBsrI0Q/viewform','data':'data.json'},'De Voorspellingschecker',NLMETA))
open(os.path.join(out,'en_public.html'),'w',encoding='utf-8').write(public(en,{'tipUrl':'https://docs.google.com/forms/d/1hzlLb6BLX0ljGePTzrmoCha9MpBU5q-fZtX-dMFlGOw/viewform','x':'predictionchk','data':'data.json'},'Prediction Checker',ENMETA))
# Dutch leftovers check in the English editor
r=subprocess.run([sys.executable,os.path.join(D,'leftover.py'),os.path.join(out,'en_editor.html'),src],capture_output=True,text=True)
left=[l for l in r.stdout.splitlines() if l.strip()]
if left:
    print('DUTCH LEFT IN ENGLISH OUTPUT (add translations to en_code.json):');print('\n'.join(left));sys.exit(2)
print('ok: nl_editor, en_editor, nl_public, en_public in',out)
