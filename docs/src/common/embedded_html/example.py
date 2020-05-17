# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.common import EmbeddedHtml

css = """
table td,th {
    border: 1px solid black;
}
table {
    border-collapse: collapse;
}
table caption {
    font-weight: bold;
}
"""

html1 = """
<button id="foo">Foo</button>
<script>
    document.getElementById("foo").onclick = function() {
        pubsubs_publish("%(id)s","click","click");
    };
</script>
"""

html2 = """
<script>
    pubsubs_subscribe("%(id)s","click",function(obj) { alert(obj); });
</script>
"""

d = Diagram()

eh1 = EmbeddedHtml(html1,css,200,120)
eh1.substituteHtml({"id":eh1.getId()})
eh2 = EmbeddedHtml(html2,css,200,120)
eh2.substituteHtml({"id":eh1.getId()})
d.add(eh1)
d.add(eh2)

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()
