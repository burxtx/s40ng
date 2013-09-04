@echo off
cls
SETLOCAL ENABLEDELAYEDEXPANSION

if exist test_automation_input.xml (
echo deleting old test_automation_input.xml
del test_automation_input.xml
echo ------------------------------------------------------------------
)
if exist focus_config.json (
echo deleting old focus_config.json
del focus_config.json
echo ------------------------------------------------------------------
)
if exist below_config.json (
echo deleting old below_config.json
del below_config.json
echo ------------------------------------------------------------------
)
set /a counter=1
echo The following CPF files were found:
rem dir/B *.cpf
FOR %%X in (*.cpf) DO (
echo !counter!: %%~nxX
set /a counter=!counter!+1
)

:loop
set /a counter=0
set /p cpf_choice="Which CPF (1,2,..,quit) should be used? "
FOR %%X in (*.cpf) DO (
 set /a counter=!counter!+1
 if %cpf_choice%==quit (GOTO :eof)
 if %cpf_choice%==!counter! (set choice=%%~nxX)
)

if exist %choice% (
echo ------------------------------------------------------------------
echo Converting CPF into test_automation_input.xml
cpf2xml4testautomation.py -i %choice% -c -m -f customer -d -o test_automation_input.xml
if exist test_automation_input.xml (
echo ------------------------------------------------------------------
echo test_automation_input.xml created successfully
echo S40NG exclusive: convert xml to json config file
python xml2json.py
if exist focus_config.json (
echo ------------------------------------------------------------------
echo focus_config.json created successfully
echo copying focus_config.json under ..\source\test_scripts
copy focus_config.json ..\source\test_scripts
)
if exist below_config.json (
echo ------------------------------------------------------------------
echo below_config.json created successfully
echo copying below_config.json under ..\source\test_scripts
copy below_config.json ..\source\test_scripts
)
)
pause
)
