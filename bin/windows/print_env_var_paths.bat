@echo off
rem Print passed environment variable (ie. PATH) split by semi-colons.

@echo off
setlocal enabledelayedexpansion

:: Check if an argument was provided
if "%~1"=="" (
    echo Usage: %0 ENV_VAR_NAME
    exit /b 1
)

:: Get the environment variable name from the argument
set "envVar=%~1"

:: Get the value of the environment variable
set "varValue=!%envVar%!"

:: Check if the environment variable is set
if "%varValue%" == "" (
    echo Environment variable %envVar% is not set.
    exit /b 1
)

:: Initialize counter
set "count=0"

:: Loop through each value in the environment variable
for %%i in ("!varValue:;=" "!") do (
    :: Increment the counter
    set /a count+=1
    
    :: Print the current value
    echo %%i
)

:: Print the total number of values
echo Total values: %count%

endlocal
