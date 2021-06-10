## Network Settigs - VBC Vacuum pumping
Beaglebones are configured at the network `10.128.40.0/24`.

## EPICS for Windows (command line)
Steps https://github.com/lnls-sirius/pydm-opi#epics-base

Download at https://epics.anl.gov/download/distributions/EPICSWindowsTools1.44-x64.msi

Append the EPICS tools to the system and local PATH (environment variable).

### OpenSSH
Steps at https://docs.microsoft.com/pt-br/windows-server/administration/openssh/openssh_install_firstuse#install-openssh-using-powershell

### Chocolatey

Steps at https://chocolatey.org/install

```
choco install git neovim
```

### Miniconda CLI

```powershell
$ProgressPreference = 'Continue'
Invoke-WebRequest -Uri https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -O Miniconda3-latest-Windows-x86_64.exe
Start-Process Miniconda3-latest-Windows-x86_64.exe
Remove-Item Miniconda3-latest-Windows-x86_64.exe
```