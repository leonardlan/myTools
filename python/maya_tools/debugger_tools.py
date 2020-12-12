from maya import cmds


def print_attrs(node=None, **kwargs):
	'''Print attributes of node(s). If no node specified, prints attributes of nodes in selection.

	Args:
		node (str or [str] or None): Maya node(s).
		attr_filter (str): Attribute filter. Only shows attributes that contain this filter.
		val_filter (str, int, float, etc): Value filter. Only shows values equal to this filter.

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
	# Remove duplicates and sort attributes.
	attrs = sorted(list(set(cmds.listAttr(node))))

	# Get filters.
	attr_filter = kwargs.get('attr_filter', None)
	has_val_filter = 'val_filter' in kwargs
	val_filter = kwargs.get('val_filter', None)

	# Loop attributes.
	count = 0
	for attr in attrs:
		# Filter by attr.
		if attr_filter and attr_filter.lower() not in attr.lower():
			continue

		plug = '{}.{}'.format(node, attr)

		# Get type.
		try:
			type_ = cmds.getAttr(plug, type=True)
		except Exception, err:
			type_ = str(err),

		# Get and print value.
		try:
			val = cmds.getAttr(plug)
		except Exception:
			# Probably a connection attribute.

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
			# Filter by value.
			if has_val_filter and (val_filter != val or type(val_filter) != type(val)):
				continue

			# Add single quote around string.
			if type_ == 'string':
				if val is not None:
					val = "'{}'".format(val)

			# Print value.
			print '{} ({}): {}'.format(attr, type_, val)

		count += 1

	print 'Found {} attr{}'.format(count, 's' if count > 1 else '')
