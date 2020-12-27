@echo off

:: pop xmenv flag
if not defined XMENV_XENV (
	goto :EOF
) else (
	set XMENV_XENV=
)

:: pop prompt style
if defined _OLD_PROMPT (
	set PROMPT=%_OLD_PROMPT%
	set _OLD_PROMPT=
)

:: pop environment settings
if defined _OLD_PATH (
	set "PATH=%_OLD_PATH%"
	set _OLD_PATH=
)

if defined PYTHONHOME (
	set PYTHONHOME=%_OLD_PYTHONHOME%
	set _OLD_PYTHONHOME=
)

if defined PYTHONPATH (
	set PYTHONPATH=%_OLD_PYTHONPATH%
	set _OLD_PYTHONPATH=
)