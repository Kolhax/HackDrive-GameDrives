@echo off
:: List all connected drives using diskpart
echo Listing all connected drives...
echo list disk > temp_script.txt
diskpart /s temp_script.txt
del temp_script.txt

:: Ask the user for which drive to use
set /p drive_number="Enter the number of the drive to use: "

:: Confirm drive selection
echo You selected Drive %drive_number%.
set /p confirm="Is this correct? (y/n): "
if /I not "%confirm%"=="y" (
    echo Exiting...
    exit /b
)
echo.
echo Make sure to keep in mind that your drive will be formated after this action
echo.
:: Ask the user for the drive name
set /p drive_name="Enter the name of the drive (e.g., Games): "

:: Clean the drive and create a new NTFS partition
(
    echo select disk %drive_number%
    echo clean
    echo create partition primary
    echo format fs=ntfs quick
    echo assign
) > diskpart_script.txt
diskpart /s diskpart_script.txt
del diskpart_script.txt

:: Get the letter of the newly assigned drive
for /f "tokens=3" %%a in ('diskpart /s list_volume.txt ^| findstr /i "Volume"') do set new_drive_letter=%%a

:: Copy contents of "GameDisk Base" to the new drive
xcopy "GameDisk Base" %new_drive_letter%:\ /e /h /k

:: Edit autorun.inf to update the label
(
    echo [autorun]
    echo label=%drive_name%
    echo icon=icon.ico
) > %new_drive_letter%:\autorun.inf

:: Update GameDrive.ini
(
    echo [DiskInfo]
    echo DiskName=%drive_name%
) > %new_drive_letter%:\GameDrive.ini

echo Drive setup complete! The drive %drive_name% is now ready.
pause
exit /b
