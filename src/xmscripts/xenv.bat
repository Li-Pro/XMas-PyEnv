@echo off

:: push xmenv flag
set XMENV_XENV=2020 Xmas PyEnv


:: push codepage
for /f "tokens=2 delims=:." %%a in ('where CHCP') do (
	set _CHCP_PROG=%%a
)

for /f "tokens=2 delims=:." %%a in ('CHCP') do (
	set _OLD_CDPG=%%a
)

%_CHCP_PROG% 65001 > nul


:: push prompt style
if defined PROMPT (
	set _OLD_PROMPT=%PROMPT%
) else (
	set PROMPT=$p$g
)

set PROMPT=$c%--XM_ENVNAME%$f %PROMPT%


:: push the environment settings
set _OLD_PATH=%PATH%

if defined PYTHONHOME (
	set _OLD_PYTHONHOME=%PYTHONHOME%
)

if defined PYTHONPATH (
	set _OLD_PYTHONPATH=%PYTHONPATH%
)

set PATH=%--XM_ENVPATHS%
set PYTHONHOME=
set PYTHONPATH=


:: pop codepage
%_CHCP_PROG% %_OLD_CDPG% > nul
set _CHCP_PROG=
set _OLD_CDPG=