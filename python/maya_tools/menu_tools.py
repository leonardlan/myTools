'''My Tools for creating menus in Maya.'''

from maya import cmds, mel

from maya_tools import debugger_tools


def get_main_window():
    '''Returns Maya main window.'''
    return mel.eval('$gMainWindow = $gMainWindow')


def delete_menu(label_or_path, main_window=None):
    '''Deletes menu by label or path of UI.'''
    if cmds.lsUI(label_or_path):
        cmds.deleteUI(label_or_path)
        return

    main_window = mel.eval('$gMainWindow = $gMainWindow') if main_window is None else main_window
    menus = cmds.window(main_window, query=True, menuArray=True)
    for menu in menus:
        if cmds.menu(menu, query=True, label=True) == label_or_path:
            cmds.deleteUI(menu)
            break


def create_my_menu():
    '''Create my menu.'''
    label = 'My Tools'
    delete_menu(label)

    # Create menu.
    main_window = get_main_window()
    menu = cmds.menu(parent=main_window, label=label, tearOff=True)

    cmds.menuItem(parent=menu, divider=True, dividerLabel='Attributes')

    # Create menu items.
    cmds.menuItem(
        parent=menu,
        label='Print Attributes',
        annotation='Print Attributes of Currently Selected Node',
        command=print_attrs)
    cmds.menuItem(
        parent=menu,
        label='defaultRenderGlobals',
        annotation='Print Attributes of defaultRenderGlobals',
        command=print_attrs_default_render_globals)
    cmds.menuItem(
        parent=menu,
        label='vraySettings',
        annotation='Print Attributes of vraySettings',
        command=print_attrs_vray_settings)

    cmds.menuItem(
        parent=menu,
        label='Diff Two Nodes',
        annotation='View Difference Between Two Selected Nodes',
        command=diff_two_nodes)

    cmds.menuItem(parent=menu, divider=True, dividerLabel='Debug')

    cmds.menuItem(
        parent=menu,
        label='Print args',
        annotation='Print args passed to command function',
        command=print_args)

    return menu


# Actions.


def print_attrs(args):
    '''Print Attributes of Currently Selected Node'''
    reload(debugger_tools)
    debugger_tools.print_attrs()


def print_attrs_default_render_globals(args):
    '''Print Attributes of defaultRenderGlobals'''
    reload(debugger_tools)
    debugger_tools.print_attrs_for_single_node('defaultRenderGlobals')


def print_attrs_vray_settings(args):
    '''Print Attributes of vraySettings'''
    reload(debugger_tools)
    debugger_tools.print_attrs_for_single_node('vraySettings')


def diff_two_nodes(args):
    '''View Difference Between Two Selected Nodes'''
    reload(debugger_tools)
    debugger_tools.diff()


def print_args(args):
    '''Print args.'''
    print args
