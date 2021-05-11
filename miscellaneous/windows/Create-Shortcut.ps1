$DistPath = "$Home\Documents\pydm-opi\miscellaneous\windows"
$IcoUrl = "https://github.com/lnls-sirius/pydm-opi/raw/master/miscellaneous/windows/lnls.ico"
$IcoDestPath = "$Home\Icons\"

function CreateShortcut {
    param ( [string]$DistPath, [string]$DestinationPath, [string]$Desc )

    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($DestinationPath)
    $Shortcut.TargetPath = "powershell"
    $Shortcut.Arguments = "-Command conda activate py36; pythonw.exe (Get-Command sirius-hla-as-ap-conlauncher.py).Path"
    $Shortcut.IconLocation = "$IcoDestPath\lnls.ico"
    $Shortcut.Description = "$Desc"
    $Shortcut.Save()
}

New-Item -ItemType Directory -Force -Path "$IcoDestPath"
Invoke-WebRequest -Uri $IcoUrl -OutFile "$IcoDestPath\lnls.ico"
CreateShortcut $DistPath "$Home\Desktop\Sirius PyDM OPI.lnk" "Sirius PyDM OPI Launcher"