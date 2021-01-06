# main.py
from pathlib import Path
import gettext
# _ = gettext.gettext
# fr = gettext.translation('base', localedir='locales', languages=['fr'])
# fr.install()
# _ = fr.gettext # Greek
localdir = Path(__file__).resolve().parents[2] / 'locales'
print(localdir)
gettext.install('foo', localedir=localdir)

def print_some_strings():
    print(_("Hello world"))
    print(_("This is a translatable string"))

if __name__=='__main__':
    print_some_strings()
