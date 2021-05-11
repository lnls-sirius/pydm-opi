## Network Settigs - VBC Vacuum pumping
Beaglebones are configured at the network `10.128.40.0/24`.

## EPICS for Windows (cli)
Steps https://github.com/lnls-sirius/pydm-opi#epics-base

Download at https://epics.anl.gov/download/distributions/EPICSWindowsTools1.44-x64.msi

Append the EPICS tools to the system and local PATH (environment variable).

## Python
Setup as described https://github.com/lnls-sirius/pydm-opi#install.

### Miniconda

Download at https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe

**Important**

- Local installation (single user only).
- Add to the PATHAdicionar ao PATH.

Create a conda environment using Python 3.6

```powershell
$ProgressPreference = 'Continue'
Invoke-WebRequest -Uri https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -O Miniconda3-latest-Windows-x86_64.exe
Start-Process Miniconda3-latest-Windows-x86_64.exe
# Start-Process /wait "" Miniconda3-latest-Windows-x86_64.exe /AddToPath=1 /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\Miniconda3
Remove-Item Miniconda3-latest-Windows-x86_64.exe
```

```command
conda create --name py36 python=3.6
```

Environment dependencies:
```command
conda init powershell
conda activate py36
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install qt==5.12.9 pyqt==5.12.3 pydm==1.10.4

pip install siriushlacon
```

### OpenSSH
Steps at https://docs.microsoft.com/pt-br/windows-server/administration/openssh/openssh_install_firstuse#install-openssh-using-powershell

### Chocolatey

Steps at https://chocolatey.org/install

```
choco install git neovim
```

## Shortcut
```powershell
iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/lnls-sirius/pydm-opi/master/miscellaneous/windows/Create-Shortcut.ps1'));
```
