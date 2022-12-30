from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.nodes import Body, Element


class abcnotationblock(Body, Element):
    pass


class AbcNotation(Directive):

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self):
        node = abcnotationblock()

        lines = []
        for line in self.content:
            lines += [f'"{line}\\n"']
        node["abctext"] = "+\n          ".join(lines)
        return [node]


def html_abcblock(self, node):
    """
    Convert block to the script here.
    """
    from uuid import uuid4

    template = """
<div id="paper-%(random)s"></div>
<script type="text/javascript">
var abc = %(abctext)s
ABCJS.renderAbc("paper-%(random)s", abc);
</script>
"""
    self.body.append(template % {"random": uuid4(), "abctext": node["abctext"]})
    raise nodes.SkipNode


def setup(app):

    app.add_node(abcnotationblock, html=(html_abcblock, None))

    app.add_directive("abcnotation", AbcNotation)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
