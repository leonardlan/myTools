(setq markdown-xhtml-header-content
      "<style type='text/css'>
img {
    vertical-align: middle;
    width: 32px;
    height: 32px
}
</style>")

<title>Debug Checklist</title>

# Debug Checklist

The things I've learned throughout years of debugging failed renders and bugs. Maybe one day this will be scripted and no longer require TDs. :smile:

## :computer:Service not found or failing
- Check logs on client machine
- Try accessing via browser
- Check other URLs in web app
- Try pinging the service `ping MACHINE_NAME`
- `ssh` into machine
    - Check service status
    - Check logs
    - File system not set up or mounted correctly. See `df -h`
    - Check fstab `cat /etc/fstab` set up correctly
    - Restart service as correct user

## Farm Issues
### Render failing on farm:disappointed:
#### Try:
- Check hosts to see if it's happening on a [specific machine](#specific-machine-not-working)
- Check time started to see if it's happening around the same time (Might be related to when something else broke)
- Check memory usage to see where it is peaking
- Check stdout and stderr logs for error code and traceback
    - Check for pattern in logs among failed renders. (ie. Maybe they all were killed on a certain frame)
- Check output renders with `rv output.exr`. List size. If zero, render failed.
- `ssh` into machines and check status of rendering process
- Check farm and local machine are using same version of software (ie. Nuke 10 on submitter but Nuke 9 on farm)
- Run render command locally
- Run render command as render user on remote machine that failed
- Diff env var on farm and local
- Run on higher CPU machine

#### Reasons for failure:
- No Camera present in scene
- [No license found](#No-available-license) for renderer or plug-in (ie. Nuke Optical Flare)
- License server going down may cause render to stop and sleep indefinitely. Example Katana log:
```
[ INFO     ] R50004 {WARNING} License warning - code 113: No route to host
[ INFO     ] R50004 {CONTINUED} license source: port@machine.name
[ INFO     ] R50004 {WARNING} License warning - license server connection re-established
```
```
[ INFO     ] R50004 {WARNING} License warning - code 104: Connection reset by peer
[ INFO     ] R50004 {CONTINUED} license source: port@machine.name
[ INFO     ] R50004 {WARNING} License warning - code 111: Connection refused
[ INFO     ] R50004 {CONTINUED} license source: port@machine.name
[ INFO     ] R50004 {WARNING} License warning - license server connection re-established
```

#### Possible:
- File system not set up or mounted correctly. See `df -h`
- Permission denied. Run `777 PATH_TO_FILE_OR_FOLDER`
- Cannot connect to a server
- Machine ran out of memory. Try higher capacity machine.
- [No available license](#no-available-license)

### Instance taking longer than others
#### Try:
- Check [Render failing on farm](#render-failing-on-farm) first
- Meld log with a normal instance
- ssh into machine and monitor process status
- Check if it's hanging on a specific frame
- Check output render and see which frames are not rendered

#### Possible solutions:
- Kill and restart the instance
OR
- Kill the job and submit another job rendering just the missing frame(s)

### Specific machine not working
- Check if the machine is updated to pipeline tools
- Check file system set up or mounted correctly. See `df -h`
- Check file system has enough space. See `df -h`. Run `du -hs * | sort -h` to see space usage.
- Try rebooting the machine: `ssh root@machine reboot`
- Omit the machine in render job
- Write ticket to Systems/IT

### Some render frames fail while others don't
- Check output permissions are same. If not, check mask (umask) of machines that rendered the failed frames.

### No available license
- Look up license usage. Maybe there were too many renders going on at the same time maxing out licenses. Try limiting/reserving current renders available for renderer
Are we out of license?
- If it's a Nuke plug-in, try to pre-comp the node output, delete the node, and render on the farm so that it won't take up a plug-in license.
- Limit number of instances run simultaneously
- Ask ones who're not using it to close it down
- Ask to purchase more licenses
- Wait for a free license

### Command works on my machine but not others' machine
#### Try:
- Meld output of local machine with remote machine
```bash
export MACHINE_NAME=''
export COMMAND=''
meld <(ssh $MACHINE_NAME $COMMAND) <(eval $COMMAND) &
```
- Diff env var. Run the above with
```bash
export COMMAND='env'
```

#### Possible:
- Different system environment
- Missing dependencies
- Hard-coded directory or path in the code

### Farm too full
- Add unused machines (maybe someone sick or away)

### Job pending too long
- Lower instances on existing renders
- Create pool/group of machines for specific type of renders
- Lower reservations. Maybe request less processors or memory.
- If it's a fast render, temporarily assign it to a group of available machines

### Host not picking up jobs
- `ping hostname`
- `ssh hostname`

### Network file/folder symlink does not exist on a machine
- If network file/folder does not exist on a machine when it's supposed to, try rebooting it.

## <img src="https://1.bp.blogspot.com/-HGzMAuW1Neo/Wwg1DBO1nLI/AAAAAAAABvE/U8pNkz07IocDCljJVcEsvogx8bqkVpP8QCLcBGAs/s1600/Maya.png" style="background-color: transparent; vertical-align: middle; width: 32px; height: 32px"> Maya Problems
### Maya scene takes too long to open or crashes a lot
#### Possible:
- File too large
- Is there complicated texturing?
- When referencing, maya sequentially scans references and reads every file with selected options. Try referencing Maya Binary files (.mb) as they are already in Maya proprietary scene format and faster to load than Maya ASCII files.

### Maya hangs while starting up (No error)
- Check if a config file is locked up at `~/.config/Autodesk/`. Remove the lock file. This sometimes happens when maya crashed.

### Try:
- Turn off ray tracing
- Turn off Subsurface Scattering
- Turn off Anti Aliasing
- Turn off motion blur

### Optimize scene size
- Remove empty, invalid, and unused information from the scene. `Select File > Optimize Scene Size`
- Remove construction history from the selected object(s). Only do this if you are sure you do not need to edit the objects’ history again.
- Select the objects and select Edit > Delete by Type > History. Do not save panel layouts with the scene. `In the UI Elements preferences (Window > Settings/Preferences > Preferences), turn off Save Panel Layouts with File.`
- Delete static animation channels. `Edit > Delete by Type > Static Channels.`

## All Things Trivial
- Is renderman globals node deleted?
- Check if SELinux is enabled. `sestatus`. Try disabling it: `setenforce 0`
- Try disabling firewall on remote server
- Non-breaking space (also called no-break space, non-breakable space (NBSP), hard space, or fixed space): " "
    A space character that prevents an automatic line break at its position. In Unicode it is encoded as U+00a0.
    It looks like a space but it's not.
    (╯°□°）╯︵ ┻━┻
- Latest code is pushed to production repo but not deployed

## General debug
- Try closing and opening the software:laughing:
