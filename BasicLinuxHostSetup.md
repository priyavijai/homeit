
** Everything here is applicable to Ubuntu server LTS systems. **

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

# SSH Key

If you don't already have a SSH key, you can generate a default one by running:

`ssh-keygen -t rsa -C "email@wherever.whatever"`

The defaults work fine (no password, `$HOME/.ssh/id_rsa` and `$HOME/.ssh/id_rsa.pub`).

The file `$HOME/.ssh/id_rsa.pub` contains the public key. The entire text as is can be added to places like GitHub to configure SSH based authentication. The private key should be copied to wherever you need to SSH from such as Putty clients etc.






