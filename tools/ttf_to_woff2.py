import sys
import json
import os.path

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable

# pip3 install fonttools
# pip3 install brotli

def convert(ttf_path,weight,style):
    woff2_path = os.path.splitext(ttf_path)[0]+".woff2"
    json_path = os.path.splitext(ttf_path)[0]+".json"
    # https://stackoverflow.com/questions/4190667/how-to-get-width-of-a-truetype-font-character-in-1200ths-of-an-inch-with-python
    font = TTFont(ttf_path)
    cmap = font['cmap']
    t = cmap.getcmap(3,1).cmap
    s = font.getGlyphSet()
    units_per_em = font['head'].unitsPerEm
    
    widths = {}
    for code in t:
        if t[code] in s:
            widths[str(chr(code))] = s[t[code]].width/units_per_em
    d = { "glyph_widths":widths, "weight":weight, "style":style }
    open(json_path,"w").write(json.dumps(d))
    font.flavor = "woff2"
    font.save(woff2_path)

if __name__ == '__main__':
    path = sys.argv[1]
    weight = sys.argv[2]
    style = sys.argv[3]
    convert(path,weight,style)
    