from maya import cmds


def print_all_attrs(node, **kwargs):
    """ Print name, type, and value of attributes of a maya node """
    for attr in sorted(cmds.listAttr(node, **kwargs)):
        attr_name = "%s.%s" % (node, attr)
        try:
            typ = cmds.getAttr(attr_name, type=True),
        except Exception, e:
            typ = str(e),
        print attr_name, "(%s) =" % typ,
        try:
            print cmds.getAttr(attr_name)
        except Exception, e:
            print "%r" % e
