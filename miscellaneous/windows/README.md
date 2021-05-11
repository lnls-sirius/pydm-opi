## Configuração REDE
Beaglebones estão configuradas na subrede `10.128.40.0/24`.

## EPICS para Windows (cli)
Passos em https://github.com/lnls-sirius/pydm-opi#epics-base

Download em https://epics.anl.gov/download/distributions/EPICSWindowsTools1.44-x64.msi

Após a instalação, adicionar local ao PATH do Windows.

## Ambiente Python
Configurar ambiente seguindo passos de https://github.com/lnls-sirius/pydm-opi#install, Miniconda é recomendado.

### Miniconda

Download em https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe

- Escolher instalação local (apenas para o usuário).
- Adicionar ao PATH do sistema.

Criar o ambiente conda usando Python 3.6

```command
conda create --name py36 python=3.6
```

Instalando dependências do ambiente:
```command
conda init powershell
conda activate py36
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install qt==5.12.9 pyqt==5.12.3 pydm==1.10.4

pip install siriushlacon
```

## Etc.
Configurar programa padrão usado na execução de arquivos `.py`, apontar para o Python do ambiente virtual.

### OpenSSH
Passos em https://docs.microsoft.com/pt-br/windows-server/administration/openssh/openssh_install_firstuse#install-openssh-using-powershell

```powershell
Get-WindowsCapability -Online | ? Name -like 'OpenSSH*'
```

```powershell
# Install the OpenSSH Client
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0

# Install the OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

```powershell
Start-Service sshd
# OPTIONAL but recommended:
Set-Service -Name sshd -StartupType 'Automatic'
# Confirm the firewall rule is configured. It should be created automatically by setup.
Get-NetFirewallRule -Name *ssh*
# There should be a firewall rule named "OpenSSH-Server-In-TCP", which should be enabled
# If the firewall does not exist, create one
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

### Chocolatey

Passos em https://chocolatey.org/install

```
choco install git neovim
```

## Criar atalho
```powershell
iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/lnls-sirius/pydm-opi/master/miscellaneous/windows/Create-Shortcut.ps1'))
```
