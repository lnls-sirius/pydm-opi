$IcoUrl = "https://github.com/lnls-sirius/pydm-opi/raw/master/miscellaneous/windows/"
$IcoDestPath = "$Home\Icons\"
$ShortcutName = "Sirius PyDM OPI.lnk"

$IcoLnls = "lnls.ico"
$IcoSirius = "sirius.ico"

New-Item -ItemType Directory -Force -Path "$IcoDestPath"

Invoke-WebRequest -Uri "$IcoUrl/$IcoLnls"   -OutFile "$IcoDestPath\$IcoLnls"
Invoke-WebRequest -Uri "$IcoUrl/$IcoSirius" -OutFile "$IcoDestPath\$IcoSirius"

function CreateShortcut {
    param ( [string]$DestinationPath, [string]$Ico, [string]$Desc, [string]$Script )

    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($DestinationPath)
    $Shortcut.TargetPath = "powershell"
    $Shortcut.Arguments = "-Command conda activate py36; pythonw.exe (Get-Command $Script).Path"
    $Shortcut.IconLocation = "$IcoDestPath\$Ico"
    $Shortcut.Description = "$Desc"
    $Shortcut.Save()
}

CreateShortcut "$Home\Desktop\Sirius PyDM OPI.lnk" $IcoLnls "Sirius PyDM OPI Launcher" "sirius-hla-as-ap-conlauncher.py"
CreateShortcut "$Home\Desktop\VBC.lnk" $IcoSirius "VBC" "sirius-hla-as-va-vbc.py"
