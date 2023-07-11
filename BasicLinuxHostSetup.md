
**Everything here is applicable to Ubuntu server LTS systems.**

**NOTE: This setup is only for a host intended to run PiHole and Unifi controller.**

# Password Less SUDO

Passwordless SUDO is very useful. 

`sudo groupadd -g adm $USERNAME`

This will add the user to the `adm` group.

Then modify sudo configuration by running `sudo visudo`. This will open the sudo configuration in the Nano editor (or is it Pico?)

Modify the line that looks like:

```
# Members of the admin group may gain root privileges
%admin ALL=(ALL) ALL:ALL
```
to look like

```
# Members of the admin group may gain root privileges
%adm ALL=(ALL) NOPASSWD:ALL
```

This will enable anyone in the `adm` group to perform `sudo` without being prompted for a password.

# Remove CDROM APT source

I install from a CDROM and that usually configures the CDROM as a APT source. This can be problematic later when the CDROM is no longer available. Right after installing a new system, typically only the CDROM source is in `/etc/apt/sources.list` so it can just be truncated with:

`sudo truncate -s 0 /etc/apt/sources.list`

# Force Different DNS Nameservers

This is useful to force use of specific nameservers. I use this as a precursor to running pihole in a Docker container.

First force link `/etc/resolv.conf` to the `systemd-resolved` generated one:

`sudo unlink /etc/resolv.conf`
`sudo ln -sv /run/systemd/resolve/resolv.conf /etc/resolv.conf`

Then update `/etc/systemd/resolved.conf` as follows (you can play with the options):

```
[Resolve]
DNS=1.1.1.1 1.0.0.1
FallbackDNS=8.8.8.8 8.8.4.4
DNSSEC=yes
DNSOverTLS=yes
Cache=no-negative
DNSStubListener=no
ReadEtcHosts=yes
```

Then restart the `systemd-resolved` service:

`sudo systemctl restart systemd-resolved`

Verify DNS lookups continue to work correctly by checking the output of:

`nslookup www.google.com`

# Some Useful Basic Software

`git` is typically already installed.
`docker` can be installed with `sudo apt install -y docker.io`
`brutil` can be installed with `sudo apt install -y bridge-utils`
`ping` can be installed with `sudo apt install -y iputils-ping`
`ip` can be installed with `sudo apt install -y iproute2`

# SSH Key

If you don't already have a SSH key, you can generate a default one by running:

`ssh-keygen -t rsa -C "email@wherever.whatever"`

The defaults work fine (no password, `$HOME/.ssh/id_rsa` and `$HOME/.ssh/id_rsa.pub`).

The file `$HOME/.ssh/id_rsa.pub` contains the public key. The entire text as is can be added to places like GitHub to configure SSH based authentication. The private key should be copied to wherever you need to SSH from such as Putty clients etc.

# Configure Docker

Before you can use Docker commands, you have to perform additional configuration.

First, give yourself permissions to access the Docker socket.

`sudo usermod -a -G docker $USER`

Optionally create a new file at `/etc/docker/daemon.json` (or modify if it already exists). The following example shows some simple and useful options:

```
{
  "experimental": true,
  "max-concurrent-downloads": 4,
  "max-concurrent-uploads": 4,
  "debug": true,
  "log-level": "info"
}
```

Restart `docker` daemon with `sudo systemctl restart docker`.

Then **logout** and log back in and verify `docker` connectivity is working by running the following commands:

`docker ps -a`
`docker images`

Setup a MACVLAN network so that network management apps can run directly on the network. Create the network with the following command:

`docker network create -d macvlan --subnet=172.16.1.0/24 --gateway=172.16.1.1 -o parent=enp1s0 network-apps-vlan`

# Disable Sleep

Check whether the machine is setup to sleep or not with:

`systemctl status sleep.target`

If it is, then disable sleep by executing the following commands:

`sudo systemctl mask sleep.target suspend.target hibernate.target`

# Install JRE 8

Install JRE version 8 with:

`sudo apt install -y openjdk-8-jre`

Then force use of Java 8:

`sudo update-java-alternatives --jre -s java-1.8.0-openjdk-amd64`

Ensure this configuration doesn't get overriden by running:

`sudo apt-mark hold openjdk-11-*`

This can be undone by running:

`sudo apt-mark unhold openjdk-11-*`

# Install Unifi Controller

Install userland entropy generator:

`sudo apt install haveged`

Add the Ubiquiti APT sources:

`echo 'deb https://www.ui.com/downloads/unifi/debian stable ubiquiti' | sudo tee /etc/apt/sources.list`

Add the GPG key for the above:

`sudo wget -O /etc/apt/trusted.gpg.d/unifi-repo.gpg https://dl.ui.com/unifi/unifi-repo.gpg`

Then update APT cache:

`sudo apt update -y`

Install Unifi controller with:

`sudo apt install -y unifi`

Run the Unifi controller with:

`sudo service unifi start`

Set the controller to automatically start at boot with:

`sudo update-rc.d unifi defaults`

If Unifi devices are already managed by a different controller, then do the following.

- In settings, under System, under Advanced, set the IP of the new controller host.
- Log in to each device via ssh and run `set-inform http://new-ip-or-fqdn-:8080/inform` to set the controller URL.

# Install PiHole

Install PiHole with:

`curl -sSL https://install.pi-hole.net | sudo bash`

Write down the password that is shown for the admin. 

Then change the password by running:

`pihole -a -p`

Choose a new password.

Check that DNS resolution is working well by running:

`nslookup www.google.com <ip-of-dns-server>`

Add various blocking lists and then run `pihole -g` to reconfigure.










