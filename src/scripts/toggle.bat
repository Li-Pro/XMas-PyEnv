@echo off

if not defined XMENV_XENV (
	xenv.bat
) else (
	menv.bat
)