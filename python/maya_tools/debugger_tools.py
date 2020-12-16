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
	# Remove duplicates and sort attributes.
	attrs = sorted(list(set(cmds.listAttr(node))))

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
				elif val_filter != val or type(val_filter) != type(val):
					# Match by same type and value.
					continue

			# Add single quote around string.
			if typ == 'string':
				if val is not None:
					val = "'{}'".format(val)

			# Print value.
			print '{} ({}): {}'.format(attr, typ, val)

		count += 1

	print 'Found {} attr{}'.format(count, 's' if count > 1 else '')
