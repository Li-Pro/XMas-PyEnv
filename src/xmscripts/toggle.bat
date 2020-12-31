@echo off

if not defined XMENV_XENV (
	"%~dp0"\xenv.bat
) else (
	"%~dp0"\menv.bat
)