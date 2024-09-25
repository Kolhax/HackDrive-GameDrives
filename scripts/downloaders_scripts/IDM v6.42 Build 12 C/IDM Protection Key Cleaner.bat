@Echo OFF
set /a _Debug=0
::==========================================
@Echo OFF
:: AveYo: define USER before asking for elevation since it gets replaced for limited accounts
@if not defined USER for /f "tokens=2" %%s in ('whoami /user /fo list') do set "USER=%%s">nul
:: AveYo: ask for elevation passing arguments
@set "_=set USER=%USER%&&call "%~f0" %*"&reg query HKU\S-1-5-19>nul 2>nul||(
@powershell -nop -c "start -verb RunAs cmd -args '/d/x/q/r',$env:_"&exit)

::==========================================
CLS
Echo OFF
Color 07
Title IDM Protection Key Cleaner
Echo::========================================================================================
Echo::
Echo::== IDM Protection Key Cleaner (Based on IDM FS Cleaner v20.10.13) ======================
Echo::
Echo::== Contributors: @WindowsAddict, @BTJB, @Saheen ========================================
Echo::
Echo::========= Developer and Author: @yaschir ===============================================
Echo::
Echo::===== * Special thanks to the Contributors * ===========================================
Echo::
Echo::========================================================================================

Echo:
::CALLScript
CALL :ScriptA
CALL :ScriptEND

goto :eof

::
:ScriptA
::------------------------------------------------------------------------------------------------------------------------------------
::Reg-entries cleaning
::------------------------------------------------------------------------------------------------------------------------------------
set "nul=1>nul 2>nul"
setlocal EnableDelayedExpansion

for %%# in (
"HKLM\Software\Classes\CLSID\{7B8E9164-324D-4A2E-A46D-0165FB2000EC}"
"HKLM\Software\Classes\CLSID\{6DDF00DB-1234-46EC-8356-27E7B2051192}"
"HKLM\Software\Classes\CLSID\{D5B91409-A8CA-4973-9A0B-59F713D25671}"
"HKLM\Software\Classes\CLSID\{5ED60779-4DE2-4E07-B862-974CA4FF2E9C}"
"HKLM\Software\Classes\CLSID\{07999AC3-058B-40BF-984F-69EB1E554CA7}"
"HKLM\Software\Classes\CLSID\{E8CF4E59-B7A3-41F2-86C7-82B03334F22A}"
"HKLM\Software\Classes\CLSID\{9C9D53D4-A978-43FC-93E2-1C21B529E6D7}"
"HKLM\Software\Classes\CLSID\{79873CC5-3951-43ED-BDF9-D8759474B6FD}"
"HKLM\Software\Classes\CLSID\{E6871B76-C3C8-44DD-B947-ABFFE144860D}"
"HKLM\Software\Classes\Wow6432Node\CLSID\{7B8E9164-324D-4A2E-A46D-0165FB2000EC}"
"HKLM\Software\Classes\Wow6432Node\CLSID\{6DDF00DB-1234-46EC-8356-27E7B2051192}"
"HKLM\Software\Classes\Wow6432Node\CLSID\{D5B91409-A8CA-4973-9A0B-59F713D25671}"
"HKLM\Software\Classes\Wow6432Node\CLSID\{5ED60779-4DE2-4E07-B862-974CA4FF2E9C}"
"HKLM\Software\Classes\Wow6432Node\CLSID\{07999AC3-058B-40BF-984F-69EB1E554CA7}"
"HKLM\Software\Classes\Wow6432Node\CLSID\{E8CF4E59-B7A3-41F2-86C7-82B03334F22A}"
"HKLM\Software\Classes\Wow6432Node\CLSID\{9C9D53D4-A978-43FC-93E2-1C21B529E6D7}"
"HKLM\Software\Classes\Wow6432Node\CLSID\{79873CC5-3951-43ED-BDF9-D8759474B6FD}"
"HKLM\Software\Classes\Wow6432Node\CLSID\{E6871B76-C3C8-44DD-B947-ABFFE144860D}"
"HKCU\Software\Classes\CLSID\{7B8E9164-324D-4A2E-A46D-0165FB2000EC}"
"HKCU\Software\Classes\CLSID\{6DDF00DB-1234-46EC-8356-27E7B2051192}"
"HKCU\Software\Classes\CLSID\{D5B91409-A8CA-4973-9A0B-59F713D25671}"
"HKCU\Software\Classes\CLSID\{5ED60779-4DE2-4E07-B862-974CA4FF2E9C}"
"HKCU\Software\Classes\CLSID\{07999AC3-058B-40BF-984F-69EB1E554CA7}"
"HKCU\Software\Classes\CLSID\{E8CF4E59-B7A3-41F2-86C7-82B03334F22A}"
"HKCU\Software\Classes\CLSID\{9C9D53D4-A978-43FC-93E2-1C21B529E6D7}"
"HKCU\Software\Classes\CLSID\{79873CC5-3951-43ED-BDF9-D8759474B6FD}"
"HKCU\Software\Classes\CLSID\{E6871B76-C3C8-44DD-B947-ABFFE144860D}"
"HKCU\Software\Classes\Wow6432Node\CLSID\{7B8E9164-324D-4A2E-A46D-0165FB2000EC}"
"HKCU\Software\Classes\Wow6432Node\CLSID\{6DDF00DB-1234-46EC-8356-27E7B2051192}"
"HKCU\Software\Classes\Wow6432Node\CLSID\{D5B91409-A8CA-4973-9A0B-59F713D25671}"
"HKCU\Software\Classes\Wow6432Node\CLSID\{5ED60779-4DE2-4E07-B862-974CA4FF2E9C}"
"HKCU\Software\Classes\Wow6432Node\CLSID\{07999AC3-058B-40BF-984F-69EB1E554CA7}"
"HKCU\Software\Classes\Wow6432Node\CLSID\{E8CF4E59-B7A3-41F2-86C7-82B03334F22A}"
"HKCU\Software\Classes\Wow6432Node\CLSID\{9C9D53D4-A978-43FC-93E2-1C21B529E6D7}"
"HKCU\Software\Classes\Wow6432Node\CLSID\{79873CC5-3951-43ED-BDF9-D8759474B6FD}"
"HKCU\Software\Classes\Wow6432Node\CLSID\{E6871B76-C3C8-44DD-B947-ABFFE144860D}"
"HKU\.DEFAULT\Software\Classes\CLSID\{7B8E9164-324D-4A2E-A46D-0165FB2000EC}"
"HKU\.DEFAULT\Software\Classes\CLSID\{6DDF00DB-1234-46EC-8356-27E7B2051192}"
"HKU\.DEFAULT\Software\Classes\CLSID\{D5B91409-A8CA-4973-9A0B-59F713D25671}"
"HKU\.DEFAULT\Software\Classes\CLSID\{5ED60779-4DE2-4E07-B862-974CA4FF2E9C}"
"HKU\.DEFAULT\Software\Classes\CLSID\{07999AC3-058B-40BF-984F-69EB1E554CA7}"
"HKU\.DEFAULT\Software\Classes\CLSID\{E8CF4E59-B7A3-41F2-86C7-82B03334F22A}"
"HKU\.DEFAULT\Software\Classes\CLSID\{9C9D53D4-A978-43FC-93E2-1C21B529E6D7}"
"HKU\.DEFAULT\Software\Classes\CLSID\{79873CC5-3951-43ED-BDF9-D8759474B6FD}"
"HKU\.DEFAULT\Software\Classes\CLSID\{E6871B76-C3C8-44DD-B947-ABFFE144860D}"
"HKU\.DEFAULT\Software\Classes\Wow6432Node\CLSID\{7B8E9164-324D-4A2E-A46D-0165FB2000EC}"
"HKU\.DEFAULT\Software\Classes\Wow6432Node\CLSID\{6DDF00DB-1234-46EC-8356-27E7B2051192}"
"HKU\.DEFAULT\Software\Classes\Wow6432Node\CLSID\{D5B91409-A8CA-4973-9A0B-59F713D25671}"
"HKU\.DEFAULT\Software\Classes\Wow6432Node\CLSID\{5ED60779-4DE2-4E07-B862-974CA4FF2E9C}"
"HKU\.DEFAULT\Software\Classes\Wow6432Node\CLSID\{07999AC3-058B-40BF-984F-69EB1E554CA7}"
"HKU\.DEFAULT\Software\Classes\Wow6432Node\CLSID\{E8CF4E59-B7A3-41F2-86C7-82B03334F22A}"
"HKU\.DEFAULT\Software\Classes\Wow6432Node\CLSID\{9C9D53D4-A978-43FC-93E2-1C21B529E6D7}"
"HKU\.DEFAULT\Software\Classes\Wow6432Node\CLSID\{79873CC5-3951-43ED-BDF9-D8759474B6FD}"
"HKU\.DEFAULT\Software\Classes\Wow6432Node\CLSID\{E6871B76-C3C8-44DD-B947-ABFFE144860D}"
) do for /f "tokens=* delims=" %%A in ("%%#") do (
set "reg=%%#" &CALL :DELETE
)

Echo: 
Exit /b

:DELETE

REG DELETE %reg% /f %nul%

if [%errorlevel%]==[0] (
set "status=powershell write-host 'Deleted ' -fore '"Green"' -NoNewline; write-host '""%reg%""' -fore '"White"'"
) else (
set "status=echo Not found %reg%"
)

reg query %reg% %nul%

if [%errorlevel%]==[0] (
set "status=powershell write-host 'Deleted by taking ownership ' -fore '"Yellow"' -NoNewline; write-host '""%reg%""' -fore '"White"'"
%nul% CALL :reg_takeownership "%reg%" "ReadPermissions, ReadKey" Allow %USER%
%nul% CALL :reg_takeownership "%reg%" "SetValue, Delete" Deny S-1-5-32-544 S-1-5-18

for /f "tokens=2 delims=:" %%s in ('sc showsid TrustedInstaller ^|findstr "S-1"') do set TI=%%s& call set TI=%%TI: =%%
%nul% CALL :reg_takeownership "%reg%" FullControl Allow S-1-5-32-544 %TI%
REG DELETE %reg% /f %nul%
)

reg query %reg% %nul%

if [%errorlevel%]==[0] (
powershell write-host 'Failed to delete ' -fore '"Red"' -NoNewline; write-host '""%reg%""' -fore '"White"'
) else (
%status%
)
Exit /b


:reg_takeownership          key:"HKCU\Console" perm:"FullControl" access:"Allow" user:"S-1-5-32-544" owner(optional):"S-1-5-18"
powershell -nop -c "$A='%~1','%~2','%~3','%~4','%~5';iex(([io.file]::ReadAllText('%~f0')-split':regown\:.*')[1])"&exit/b:regown:
$D1=[IO.IODescriptionAttribute].Module.GetType('System.Diagnostics.Process').GetMethods(42)|where{$_.Name-eq'SetPrivilege'}
'SeTakeOwnershipPrivilege','SeBackupPrivilege','SeRestorePrivilege' |% {$D1.Invoke($null, @("$_",2))}
$rk=$A[0]-split'\\',2; switch -regex($rk[0]){'[mM]'{$HK='LocalMachine'};'[uU]'{$HK='CurrentUser'};default{$HK='ClassesRoot'};}
$key=$rk[1];$perm='FullControl',$A[1],$A[1];$access='Allow',$A[2],$A[2];$user=0,0,0; if($A[4]-eq''){$A[4]=$A[3]} ;$sec=0,0,0
$rule=0,0,0; $sid=$A[4],$A[3],'S-1-5-32-544'; 0,1,2 |% {$user[$_]=[System.Security.Principal.SecurityIdentifier]$sid[$_]
$rule[$_]=new-object System.Security.AccessControl.RegistryAccessRule($user[$_],$perm[$_],3,1,$access[$_])
$sec[$_]=new-object System.Security.AccessControl.RegistrySecurity}; $sec[0].SetOwner($user[0]); $sec[2].SetOwner($user[2])
function Reg_Own{param($hive,$key); $reg=[Microsoft.Win32.Registry]::$hive.OpenSubKey($key,'ReadWriteSubTree','TakeOwnership')
$reg.SetAccessControl($sec[2]); $rep=$reg.OpenSubKey('','ReadWriteSubTree','ChangePermissions'); $acl=$rep.GetAccessControl()
$acl.ResetAccessRule($rule[1]); $rep.SetAccessControl($acl); $acl=$sec[0]; $reg.SetAccessControl($acl)} ;Reg_Own $HK $key
$rec=[Microsoft.Win32.Registry]::$HK.OpenSubKey($key);foreach($sub in $rec.GetSubKeyNames()){Reg_Own $HK "$($key+'\\'+$sub)"}
Get-Acl $($rk[0]+':\\'+$rk[1])|fl #:regown: A lean and mean snippet by AveYo pastebin.com/XTPt0JSC
#-_-#


::
:ScriptEND
Echo:
Echo::===================================================
Echo::
Echo::======================= End =======================
Echo::
Echo::===================================================
Echo:
Echo:
Echo:Press any key to exit... & Pause >nul & Exit

