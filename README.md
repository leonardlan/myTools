# myTools
A collection of my
  - [Bash aliases and functions](my_settings/bash_aliases)
  - [Maya scripts](maya_scripts)
  - [Python functions](pythonrc) that help with debugging in Python Interpreter
  - Tools
  - [Useful commands](docs/useful_commands.md)
  - Git preferences
  - Sublime preferences
  - Step-by-step [debug checklist](docs/debug_checklist.md) for when a render fails on the farm or a service is not working

from working as a Software Developer and Pipeline TD in VFX industry.

# Honourable Mentions
## Python Functions
### Convert Seconds to Human-Readable Time

```python
>>> from lancore import human_time
>>> human_time(15)
'15 seconds'
>>> human_time(3600)
'1 hour'
>>> human_time(3720)
'1 hour and 2 minutes'
>>> human_time(266400)
'3 days and 2 hours'
>>> human_time(-1.5)
'-1.5 seconds'
>>> human_time(0)
'0 seconds'
>>> human_time(0.1)
'100 milliseconds'
>>> human_time(1)
'1 second'
>>> human_time(1.234, 2)
'1.23 seconds'
```

## Aliases

- lssmart - Prints path to file color-indicating up to where it exists.
![lssmart](img/lssmart.png?raw=true "Lists path to file up to existing in blue and rest in red")

## Maya Scripts
[Cube of Spheres](maya_scripts/cube_of_spheres.py) creates a cube made up of spheres with input size
![Cube of Spheres](img/cube_of_spheres.png?raw=true "Cube of Spheres!!!!")

# Setup
Run `./setup.sh`

# Run Unit Tests
`nosetests`
