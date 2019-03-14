from mayatools.context import selection


with selection():
    SIZE = 5
    def foo(input):
        return -1 * (SIZE - 1) + input * 2

    result = cmds.promptDialog(
        title='Cube Of Spheres',
        message='Enter Size:',
        button=['Create', 'Cancel'],
        defaultButton='Create',
        cancelButton='Cancel',
        dismissString='Cancel',
        style="integer",
        text=SIZE
    )

    if result == 'Create':
        SIZE = int(cmds.promptDialog(query=True, text=True))
        boundaries = [0, SIZE - 1]
        for x in range(SIZE):
            for y in range(SIZE):
                for z in range(SIZE):
                    if x not in boundaries and y not in boundaries and z not in boundaries:
                        continue
                    cmds.polySphere()
                    cmds.move(foo(x), foo(y), foo(z))
