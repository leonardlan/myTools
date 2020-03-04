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
>>> human_time(1.234, decimals=2)
'1.23 seconds'
```

### Time How Long Function Call Took
Have you ever executed a time-consuming function (ie. API request, ) but you never knew **exactly** how long it took? Now you can by passing the function and its parameters to time_me():
```python
>>> import time
>>> time_me(time.sleep, 5)
Running sleep(5)
1/1 [2020-03-03 23:16:56.344147]: 5.0 seconds
```

You can also run multiple times in serial and see average time:
```python
>>> def sleep_random():
...   time.sleep(randint(1, 10))
... 
>>> time_me(sleep_random, n=5)
Running sleep_random()
1/5 [2020-03-03 23:43:06.742977]: 1.0 seconds
2/5 [2020-03-03 23:43:07.744113]: 3.0 seconds
3/5 [2020-03-03 23:43:10.746911]: 7.0 seconds
4/5 [2020-03-03 23:43:17.753933]: 2.0 seconds
5/5 [2020-03-03 23:43:19.756087]: 7.0 seconds
Total time: 20.0 seconds
Average time: 4.0 seconds
Fastest time: 1.0 seconds
Slowest time: 7.0 seconds
Standard deviation: 2.53
```

Also available as @time_me_wrapper decorator.
```python
>>> @time_me_wrapper
... def foo():
...   print 'Hi!'
...   time.sleep(1)
...   print 'Bye!'
... 
>>> foo()
Running foo()
1/1 [2020-03-04 00:06:16.968989]: Hi!
Bye!
1.0 seconds
```

## Aliases

- lssmart - Prints path to file color-indicating up to where it exists.
![lssmart](img/lssmart.png?raw=true "Lists path to file up to existing in blue and rest in red")

## Maya Scripts
[Cube of Spheres](maya_scripts/cube_of_spheres.py) creates a cube made up of spheres with input size
![Cube of Spheres](img/cube_of_spheres.png?raw=true "Cube of Spheres!!!!")

# Unit Tests
To run unit tests, execute `nosetests` in project root directory.
