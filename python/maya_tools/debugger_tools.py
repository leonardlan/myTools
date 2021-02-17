'''My tools for debugging in Maya.'''

from maya import cmds


def print_attrs(node=None, **kwargs):
    '''Print attributes of node(s). If no node specified, prints attributes of nodes in selection.

    Args:
        node (str or [str] or None): Maya node(s).
        See print_attrs_for_single_node() for kwargs.

    Raises:
        ValueError: No object matches name.
    '''
    if not node:
        selected_nodes = cmds.ls(selection=True)
        if not selected_nodes:
            print 'No node specified and nothing is selected'
            return
        node = selected_nodes

    if isinstance(node, list):
        if len(node) == 1:
            print_attrs_for_single_node(node[0], **kwargs)
        else:
            for node_ in node:
                print '{}:'.format(node_)
                print_attrs_for_single_node(node_, **kwargs)
    else:
        print_attrs_for_single_node(node, **kwargs)


def print_attrs_for_single_node(node, **kwargs):
    '''Print name, type, and value of attributes of Maya node.

    Args:
        node (str): Node.
        attr_filter (str): Attribute filter. Only shows attributes that contain this filter.
        val_filter (str, int, float, etc): Value filter. Only shows values equal to this filter.

    Raises:
        ValueError: No object matches name.
    '''
    attrs = list_attrs(node)

    # Get filters.
    attr_filter = kwargs.get('attr_filter', None)
    has_val_filter = 'val_filter' in kwargs
    val_filter = kwargs.get('val_filter', None)

    # Loop attributes.
    count = 0
    for attr in attrs:
        # Skip attributes with period. (ie. type TdataCompound)
        if '.' in attr:
            continue

        # Filter by attr.
        if attr_filter and attr_filter.lower() not in attr.lower():
            continue

        plug = '{}.{}'.format(node, attr)

        # Get type.
        try:
            typ = cmds.getAttr(plug, type=True)
        except Exception, err:
            typ = str(err),

        # Get and print value.
        try:
            val = cmds.getAttr(plug)
        except Exception:
            # Error getting attribute. Probably a connection attribute.

            # Skip if filter speciifed.
            if attr_filter or has_val_filter:
                continue

            connections = cmds.listConnections(plug, plugs=True)
            if connections:
                print '{} connected to ({}): {}'.format(
                    attr, len(connections), ', '.join(connections))
            else:
                print '{} not connected to anything'.format(attr)
        else:
            # If enum, get it as string too.
            if typ == 'enum':
                val = '{} [{}]'.format(cmds.getAttr(plug, asString=True), val)

            # Filter by value, if specified.
            if has_val_filter:
                # Skip if not same type.
                if type(val_filter) != type(val):
                    continue

                # If string, match with "in" operator.
                if isinstance(val_filter, str):
                    if val_filter.lower() not in val.lower():
                        continue
                elif val_filter != val:
                    # Match by same type and value.
                    continue

            # Add single quote around string.
            if typ == 'string':
                if val is not None:
                    val = "'{}'".format(val)

            locked = cmds.getAttr(plug, lock=True)

            # Print value.
            print '{} ({}){}: {}'.format(attr, typ, ' [locked]' if locked else '', val)

        count += 1

    print 'Found {} attr{}'.format(count, 's' if count > 1 else '')


def list_attrs(node):
    '''Sorted and unique node attributes.'''
    return sorted(list(set(cmds.listAttr(node))))


def diff(apple, orange):
    '''Shows difference(s) between two nodes.'''
    apple_attrs = list_attrs(apple)
    orange_attrs = list_attrs(orange)
    not_in_orange = []
    differences = []
    for attr in apple_attrs:
        # Skip attributes with period. (ie. type TdataCompound)
        if '.' in attr:
            continue

        # Compare with orange.
        if attr in orange_attrs:
            # Both have attribute. Check if different.

            # Get apple attribute.
            apple_plug = '{}.{}'.format(apple, attr)
            try:
                apple_val = cmds.getAttr(apple_plug)
            except RuntimeError, err:
                print 'Could not get {}: {}'.format(apple_plug, str(err).strip())
                continue

            # Get orange attribute.
            orange_plug = '{}.{}'.format(orange, attr)
            try:
                orange_val = cmds.getAttr(orange_plug)
            except RuntimeError, err:
                print 'Could not get {}: {}'.format(orange_plug, str(err).strip())
                continue

            # Print if values are different.
            if apple_val != orange_val:
                diff_str = '{}: {} ({}) | {} ({})'.format(
                    attr, apple_val, apple, orange_val, orange)
                differences.append(diff_str)

            # Print if one is locked and other is not.
            apple_plug_locked = 'locked' if cmds.getAttr(apple_plug, lock=True) else 'unlocked'
            orange_plug_locked = 'locked' if cmds.getAttr(orange_plug, lock=True) else 'unlocked'
            if apple_plug_locked != orange_plug_locked:
                diff_str = '{} is {} and {} is {}'.format(
                    apple, apple_plug_locked, orange, orange_plug_locked)
                differences.append(diff_str)

        else:
            not_in_orange.append(attr)

    # Print summary.
    if differences:
        print '\n{} difference{}:\n{}'.format(
            len(differences), 's' if len(differences) != 1 else '', '\n'.join(differences))
    else:
        print 'No differences found between {} and {}'.format(apple, orange)

    # Print attributes not in apple.
    not_in_apple = [attr for attr in orange_attrs if attr not in orange_attrs]
    if not_in_apple:
        print '\n{} attr{} not in {}: {}'.format(
            len(not_in_apple),
            's' if len(not_in_apple) != 1 else '',
            apple,
            not_in_apple)

    # Print attributes not in orange.
    if not_in_orange:
        print '\n{} attr{} not in {}: {}'.format(
            len(not_in_orange),
            's' if len(not_in_orange) != 1 else '',
            orange,
            not_in_orange)
