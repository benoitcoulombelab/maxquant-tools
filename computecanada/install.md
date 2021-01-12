# Install/Update/Delete MaxQuant tools on Compute Canada servers

:memo: *The examples use Beluga server*


#### Options

* [Requirements](#requirements)
* [Install](#install-maxquant-tools)
* [Udate](#update-maxquant-tools)
* [Delete](#delete-maxquant-tools)


## Requirements

### Connect to the server

Use SSH command inside a terminal on [Mac](https://support.apple.com/en-ca/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac), Linux or [Windows 10 (PowerShell)](https://www.howtogeek.com/662611/9-ways-to-open-powershell-in-windows-10/)

On older versions of Windows, use [Putty](https://www.putty.org)

```
ssh beluga.computecanada.ca
```

### Run the configuration script

```
curl https://raw.githubusercontent.com/benoitcoulombelab/maxquant-tools/master/install/configure.sh >> configure.sh
chmod 744 configure.sh
./configure.sh $email@ircm.qc.ca
```

Replace `$email@ircm.qc.ca` with your email address

```
rm configure.sh
source .bash_profile
```


## Install MaxQuant tools

Run installation script

```
module load maxquant
install.sh
```

Try MaxQuant

```
maxquant --help
```


## Update MaxQuant tools

Run installation script

```
module load maxquant
install.sh
```


## Delete MaxQuant tools

Run installation script with `clean` option

```
module load maxquant
install.sh clean
```
