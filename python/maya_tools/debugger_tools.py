from maya import cmds


def print_attrs(node=None, shapes=True):
	'''Print attributes of node(s). If not specified, prints selection.

	Args:
		node (str or [str] or None): Maya node(s).
		shapes (bool): Use selected shapes if True.
	'''
	if not node:
		selected_nodes = cmds.ls(selection=True)
		if not selected_nodes:
			print 'No node specified and nothing is selected'
			return

		# Get shapes.
		if shapes:
			node = []
			for selected_node in selected_nodes:
				node.extend(cmds.listRelatives(selected_node, shapes=True) or [])

	if isinstance(node, list):
		if len(node) == 1:
			print_attrs_for_single_node(node[0])
		else:
			for node_ in node:
				print '{}:'.format(node_)
				print_attrs_for_single_node(node_)
	else:
		print_attrs_for_single_node(node)


def print_attrs_for_single_node(node, **kwargs):
	'''Print name, type, and value of attributes of Maya node.'''
	ungettable_attrs = []
	# Remove duplicates and sort attributes.
	attrs = sorted(list(set(cmds.listAttr(node, **kwargs))))
	for attr in attrs:
		plug = '{}.{}'.format(node, attr)

		# Get type.
		try:
			type_ = cmds.getAttr(plug, type=True)
		except Exception, err:
			type_ = str(err),

		# Get attr.
		try:
			val = cmds.getAttr(plug)
		except Exception:
			# Maybe it's a connection?
			try:
				print '{} connected to {}'.format(attr, cmds.listConnections(plug, plugs=True))
			except Exception:
				ungettable_attrs.append(attr)
		else:
			# Add single quote around string.
			if type_ == 'string':
				if val is not None:
					val = "'{}'".format(val)

			print '{} ({}): {}'.format(attr, type_, val)

	print 'Found {} attrs'.format(len(attrs))
	if ungettable_attrs:
		print 'Could not get {} attrs: {}'.format(
			len(ungettable_attrs), ', '.join(ungettable_attrs))
