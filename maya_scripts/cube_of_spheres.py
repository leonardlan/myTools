''' Creates a cube of spheres with input size '''


SIZE = 5

def get_movement(input):
    return -1 * (SIZE - 1) + input * 2

result = cmds.promptDialog(
    title='Cube Of Spheres',
    message='Enter Size:',
    button=['Create', 'Cancel'],
    defaultButton='Create',
    cancelButton='Cancel',
    dismissString='Cancel',
    style='integer',
    text=SIZE
)

if result == 'Create':
    SIZE = int(cmds.promptDialog(query=True, text=True))
    boundaries = [0, SIZE - 1]
    for x in range(SIZE):
        move_x = get_movement(x)
        for y in range(SIZE):
            move_y = get_movement(y)
            for z in range(SIZE):
                if x not in boundaries and y not in boundaries and z not in boundaries:
                    continue
                cmds.polySphere()
                move_z = get_movement(z)
                cmds.move(move_x, move_y, move_z)
