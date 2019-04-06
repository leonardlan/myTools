# Debug checklist

## Render failing on farm
Try:
1. Check hosts to see if it's happening on a [specific machine](#specific-machine-not-working)
2. Check time started to see if it's happening around the same time (Might be related to when something else broke)
3. Check memory usage to see where it is peaking
4. Check stdout and stderr logs for error traceback
    1. Check for pattern among failed renders
5. `ssh` into machines and check status of rendering process
6. Check farm and local machine are using same version of software (ie. Nuke 10 on submitter but Nuke 9 on farm)
7. Run render command locally
8. Diff env var on farm and local
9. Run on higher CPU machine

Reasons for failure:
    - No Camera present in scene
    - No license found for renderer
    - License server going down may cause render to stop and sleep indefinitely. Example Katana log:

        2019-04-04 12:59:12,931 katana                       [ INFO     ] R50004 {WARNING} License warning - code 113: No route to host
        2019-04-04 12:59:12,931 katana                       [ INFO     ] R50004 {CONTINUED} license source: 9010@vmlic01.bron.local
        2019-04-04 13:06:52,759 katana                       [ INFO     ] R50004 {WARNING} License warning - license server connection re-established

        Render process went to sleep mode and did not recover.

Possible:
- File system not set up or mounted correctly. See `df -h`
- Permission denied. Run `777 PATH_TO_FILE_OR_FOLDER`
- Cannot connect to a server
- Machine ran out of memory
- No available license

## Instance taking longer than others
Try:
1. Check [Render failing on farm](#render-failing-on-farm) first
1. Meld log with a normal instance
2. ssh into machine and monitor process status
3. Check if it's hanging on a specific frame
4. Check output render and see which frames are not rendered

Possible solutions:
- Kill and restart the instance
OR
- Kill the job and submit another job rendering just the missing frame(s)

## Specific machine not working
- Check if the machine is updated to pipeline tools
- Check file system set up or mounted correctly. See `df -h`
- Try rebooting the machine: `ssh root@machine reboot`
- Omit the machine in render job
- Write ticket to Systems/IT

## Some render frames fail while others don't
1. Check output permissions are same. If not, check mask (umask) of machines that rendered the failed frames.

## No available license
1. Look up license usage
Maybe there were too many renders going on at the same time maxing out licenses. Try limiting/reserving current renders available for renderer
Are we out of license?
2. Ask ones who're not using it to close it down
3. Ask to purchase more licenses
4. Wait for a free license

## Command works on my machine but not others' machine
Try:
- Diff output. Run:
    ```bash
    export MACHINE_NAME=''
    export COMMAND=''
    ssh $MACHINE_NAME $COMMAND | sort > /tmp/other_machine_cmd_output.txt
    eval $COMMAND | sort > /tmp/my_machine_cmd_output.txt
    meld /tmp/other_machine_cmd_output.txt /tmp/my_machine_cmd_output.txt &
    ```
- Diff env var. Run the above with `export COMMAND='env'`

Possible:
- Different system environment
- Missing dependencies
- Hard-coded directory or path in the code

## Maya scene takes too long to open or crashes a lot
Possible:
- File too large
- Is there complicated texturing?
- When referencing, maya sequentially scans references and reads every file with selected options. Try referencing Maya Binary files (.mb) as they are already in Maya proprietary scene format and faster to load than Maya ASCII files.

Try:
- Turn off ray tracing
- Turn off Subsurface Scattering
- Turn off Anti Aliasing
- Turn off motion blur

## Optimize scene size
- Remove empty, invalid, and unused information from the scene.
            Select File > Optimize Scene Size
- Remove construction history from the selected object(s). Only do this if you are sure you do not need to edit the objects’ history again.
- Select the objects and select Edit > Delete by Type > History. Do not save panel layouts with the scene.
            In the UI Elements preferences (Window > Settings/Preferences > Preferences), turn off Save Panel Layouts with File.
- Delete static animation channels. `Edit > Delete by Type > Static Channels.`

## All Things Trivial
- Is renderman globals node deleted?
- Check if SELinux is enabled. `sestatus`. Try disabling it: `setenforce 0`
- Try disabling firewall on remote server
- Non-breaking space (also called no-break space, non-breakable space (NBSP), hard space, or fixed space): " "
    A space character that prevents an automatic line break at its position. In Unicode it is encoded as U+00a0.
    It looks like a space but it's not.
    (╯°□°）╯︵ ┻━┻

## General debug
- Try closing and opening the software

## Service not found or failing
1. Try pinging the service `ping MACHINE_NAME`
2. File system not set up or mounted correctly. See `df -h`
