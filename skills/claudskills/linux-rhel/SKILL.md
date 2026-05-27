---
name: linux-rhel
description: Red Hat Enterprise Linux (RHEL 7/8/9) and compatible distros (CentOS, AlmaLinux, Rocky). Covers systemd (units/targets/journald), LVM (pvcreate/vgcreate/lvcreate/extend/migrate), SELinux (enforcing/permissive/audit2allow/semanage/restorecon), firewalld/iptables, nmcli/nmtui network configuration, bonding/teaming/VLANs, dnf/rpm/subscription-manager, kdump/crash analysis, performance tuning (perf/sar/vmstat/iostat/tuned), and RHEL security hardening (PAM/auditd/FIPS). Use for RHEL admin tasks, systemd troubleshooting, storage expansion, SELinux policy issues, and performance investigation.
metadata:
  author: Ryan Loiselle
  version: "1.0"
compatibility: RHEL 7, 8, 9. CentOS 7. AlmaLinux 8/9. Rocky Linux 8/9. Amazon Linux 2 where noted.
---

# Linux RHEL Skill

Red Hat Enterprise Linux administration reference — RHEL 7/8/9 focus.

**Ryan's context**: Extensive RHEL experience across versions 7, 8, and 9.

**Related skills:**
- Solaris comparison reference → [`../solaris/SKILL.md`](../solaris/SKILL.md)
- Security hardening → [`../network-security/SKILL.md`](../network-security/SKILL.md)

---

## systemd

### Unit Management

```bash
# Status and control
systemctl status <unit>              # status, recent log lines, PID
systemctl start|stop|restart|reload <unit>
systemctl enable|disable <unit>      # boot-time persistence
systemctl enable --now <unit>        # enable AND start immediately
systemctl is-active|is-enabled <unit>

# List units
systemctl list-units                 # all active units
systemctl list-units --failed        # only failed
systemctl list-unit-files            # all installed units + enabled state
systemctl list-dependencies <unit>   # dependency tree

# Reload unit files after editing
systemctl daemon-reload
```

### Unit File Locations

| Path | Purpose |
|------|---------|
| `/usr/lib/systemd/system/` | Package-installed units (do not edit) |
| `/etc/systemd/system/` | Admin overrides and custom units |
| `/run/systemd/system/` | Runtime units (transient) |

```bash
# Create a drop-in override (preferred over editing package unit)
systemctl edit <unit>                # opens drop-in editor; saves to /etc/systemd/system/<unit>.d/override.conf
systemctl edit --full <unit>         # edit full copy

# Custom service unit example
cat > /etc/systemd/system/myapp.service <<'EOF'
[Unit]
Description=My Application
After=network-online.target

[Service]
Type=simple
User=myapp
ExecStart=/opt/myapp/bin/myapp --config /etc/myapp/config.yaml
Restart=on-failure
RestartSec=5s
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload && systemctl enable --now myapp
```

### journalctl

```bash
journalctl -xe                       # recent errors, paged
journalctl -u <unit>                 # logs for specific unit
journalctl -u <unit> -f              # follow (like tail -f)
journalctl -u <unit> --since "1 hour ago"
journalctl -u <unit> --since "2024-01-01" --until "2024-01-02"
journalctl -p err -b                 # priority error and above, this boot
journalctl -b -1                     # previous boot
journalctl --disk-usage              # journal disk usage
journalctl --vacuum-size=500M        # trim journal to 500MB
journalctl --vacuum-time=30d         # trim logs older than 30 days
```

### Targets (runlevels)

| Target | Equivalent | Use |
|--------|-----------|-----|
| `poweroff.target` | runlevel 0 | Halt |
| `rescue.target` | runlevel 1 | Single user / rescue |
| `multi-user.target` | runlevel 3 | Multi-user no GUI |
| `graphical.target` | runlevel 5 | Multi-user with GUI |
| `reboot.target` | runlevel 6 | Reboot |
| `emergency.target` | — | Emergency shell (read-only root) |

```bash
systemctl get-default                # show current default target
systemctl set-default multi-user.target
systemctl isolate rescue.target      # switch to target immediately (like telinit)
```

---

## LVM — Logical Volume Manager

```bash
# Inspect
pvdisplay / pvs                      # physical volumes
vgdisplay / vgs                      # volume groups
lvdisplay / lvs                      # logical volumes
lsblk -f                             # block devices + filesystems

# Create new VG + LV
pvcreate /dev/sdb
vgcreate datavg /dev/sdb
lvcreate -n datalv -L 50G datavg
mkfs.xfs /dev/datavg/datalv
echo "/dev/datavg/datalv /data xfs defaults 0 0" >> /etc/fstab
mount /data

# Extend LV (online if filesystem supports it)
lvextend -L +20G /dev/datavg/datalv          # extend by 20GB
lvextend -l +100%FREE /dev/datavg/datalv     # use all free

# Grow filesystem after extension
xfs_growfs /data                     # XFS — online, use mountpoint
resize2fs /dev/datavg/datalv         # ext4 — online supported

# Add a new disk to existing VG
pvcreate /dev/sdc
vgextend datavg /dev/sdc

# Remove a PV from VG (move data off first)
pvmove /dev/sdb                      # migrate extents off /dev/sdb
vgreduce datavg /dev/sdb
pvremove /dev/sdb

# Take LV snapshot
lvcreate -L 5G -s -n datalv-snap /dev/datavg/datalv

# Thin provisioning
lvcreate -T -L 100G datavg/thinpool
lvcreate -V 200G -T datavg/thinpool -n thinlv1
```

---

## SELinux

```bash
# Mode management
getenforce                           # Enforcing / Permissive / Disabled
setenforce 0                         # Set permissive (temporary; until reboot)
setenforce 1                         # Set enforcing
# Permanent: edit /etc/selinux/config → SELINUX=enforcing|permissive|disabled
# Then reboot (kernel relabels on next boot when changing from disabled)

# View contexts
ls -Z /path                          # file context
ps -eZ                               # process context
id -Z                                # current user context

# Diagnose denials
ausearch -m avc -ts recent           # recent AVC denials
ausearch -m avc -ts today | audit2why  # human-readable explanation
ausearch -m avc -ts recent | audit2allow  # generate allow policy

# Apply a generated policy module
audit2allow -M mymodule < avc.log
semodule -i mymodule.pp

# Restore contexts
restorecon -Rv /path                  # restore default contexts recursively

# Manage file contexts permanently
semanage fcontext -a -t httpd_sys_content_t "/myapp(/.*)?"
restorecon -Rv /myapp

# Boolean management
getsebool -a | grep httpd            # list booleans
setsebool -P httpd_can_network_connect 1   # persistent boolean

# Port labelling
semanage port -l | grep 8080         # check what label 8080 has
semanage port -a -t http_port_t -p tcp 8080  # label a custom port

# Common SELinux context types
# httpd_sys_content_t — web content
# httpd_log_t — httpd logs
# sshd_key_t — SSH host keys
# var_log_t — generic log files
# etc_t — /etc files
```

---

## Networking with nmcli

```bash
# Show status
nmcli general status
nmcli device status
nmcli connection show                  # all configured connections

# Modify a connection
nmcli connection modify eth0 ipv4.addresses 10.0.0.5/24
nmcli connection modify eth0 ipv4.gateway 10.0.0.1
nmcli connection modify eth0 ipv4.dns "8.8.8.8 8.8.4.4"
nmcli connection modify eth0 ipv4.method manual     # static
nmcli connection modify eth0 ipv4.method auto       # DHCP
nmcli connection up eth0

# Create a new connection
nmcli connection add type ethernet ifname eth1 con-name office ipv4.method manual \
  ipv4.addresses 192.168.1.100/24 ipv4.gateway 192.168.1.1

# Bonding (active-backup mode)
nmcli connection add type bond ifname bond0 bond.options "mode=active-backup"
nmcli connection add type ethernet ifname eth0 master bond0
nmcli connection add type ethernet ifname eth1 master bond0

# LACP (mode=4)
nmcli connection add type bond ifname bond0 bond.options "mode=802.3ad,lacp_rate=fast"

# VLAN
nmcli connection add type vlan dev eth0 id 100 con-name vlan100 \
  ipv4.method manual ipv4.addresses 10.1.100.5/24

# Verify
ip addr show
ip route show
ss -tulnp                              # listening ports (replaces netstat)
```

---

## firewalld

```bash
# Zone inspection
firewall-cmd --get-default-zone
firewall-cmd --list-all                # all rules in default zone
firewall-cmd --list-all --zone=public

# Add rules (use --permanent for persistence; reload after)
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --permanent --add-port=8443/tcp
firewall-cmd --permanent --remove-port=8080/tcp
firewall-cmd --reload

# Rich rules (source-based, etc.)
firewall-cmd --permanent --add-rich-rule=\
  'rule family="ipv4" source address="10.0.0.0/8" service name="ssh" accept'

# Direct rules (raw iptables — use when rich rules insufficient)
firewall-cmd --direct --add-rule ipv4 filter INPUT 0 \
  -s 10.0.0.0/8 -p tcp --dport 443 -j ACCEPT

# Check what's open
firewall-cmd --list-services
firewall-cmd --list-ports

# Masquerade (NAT/PAT for outbound traffic)
firewall-cmd --permanent --add-masquerade
```

---

## Package Management (DNF / RPM)

```bash
# Install / remove
dnf install httpd
dnf remove httpd
dnf update                           # update all
dnf update httpd                     # update specific package
dnf autoremove                       # remove orphaned dependencies

# Search and info
dnf search nginx
dnf info httpd
dnf whatprovides /usr/bin/vim        # which package provides a file
dnf list installed
dnf list available | grep httpd

# History and rollback
dnf history list
dnf history info <id>
dnf history undo <id>                # rollback a transaction

# RPM (low-level)
rpm -qa                              # all installed packages
rpm -qi httpd                        # package info
rpm -ql httpd                        # files installed by package
rpm -qf /usr/sbin/httpd              # which package owns a file
rpm -ivh package.rpm                 # install local rpm
rpm -V httpd                         # verify package integrity

# Red Hat Subscription Manager
subscription-manager register --username=user --password=pass
subscription-manager attach --auto
subscription-manager repos --list-enabled
subscription-manager repos --enable=rhel-9-for-x86_64-appstream-rpms
```

---

## Performance Analysis

```bash
# CPU
top / htop                           # interactive
mpstat -P ALL 1 5                    # per-CPU stats, 5 samples
sar -u 1 10                          # CPU utilisation (historical + live)
perf top                             # live kernel and user-space profiling
perf record -ag sleep 10             # record 10s with call graphs
perf report                          # interactive analysis

# Memory
free -h                              # overview
vmstat -s                            # memory statistics
cat /proc/meminfo
sar -B 1 10                          # paging (major/minor faults)
slabtop                              # kernel slab allocator (caches)

# Disk I/O
iostat -xhz 2                        # extended per-device stats, 2s interval
iotop -d 2                           # per-process I/O
lsblk -io NAME,SIZE,ROTA,SCHED,TYPE  # block device tree with scheduler

# Network
sar -n DEV 1 10                      # per-interface Rx/Tx
nethogs -d 2                         # per-process bandwidth
ss -s                                # socket summary (good for connection counts)
nstat -z                             # kernel network counters

# System-wide
sar -A                               # all counters
dstat                                # combined live view
systemd-analyze blame                # boot time per service
```

### tuned Profiles

```bash
tuned-adm list
tuned-adm active
tuned-adm profile throughput-performance    # server/network tuning
tuned-adm profile latency-performance       # low-latency workloads
tuned-adm profile virtual-guest             # VM guest optimisation
tuned-adm profile balanced                  # default
```

---

## kdump / Crash Analysis

```bash
# Enable kdump
systemctl enable --now kdump
grubby --info=ALL | grep args        # verify crashkernel= in kernel args

# Trigger a crash (TEST ONLY)
echo 1 > /proc/sysrq-trigger         # sysrq must be enabled
echo c > /proc/sysrq-trigger         # kernel panic (destructive!)

# Crash dump location
ls /var/crash/

# Analyse with crash
crash /usr/lib/debug/lib/modules/$(uname -r)/vmlinux /var/crash/<timestamp>/vmcore

crash> bt              # backtrace of crashing thread
crash> log             # kernel message buffer
crash> ps             # process list at time of crash
crash> vm             # virtual memory info
crash> files          # open files
```

---

## Security Hardening

```bash
# PAM — /etc/pam.d/system-auth and /etc/pam.d/password-auth
# RHEL ships with authselect (replaces authconfig in RHEL 8+)
authselect list
authselect select sssd with-faillock   # use SSSD + account lockout

# auditd
systemctl enable --now auditd
auditctl -l                          # list active rules
auditctl -w /etc/passwd -p wa -k passwd-changes   # watch file writes/attribs
ausearch -k passwd-changes           # search audit log by key
aureport --summary                   # summary report

# Fail2ban / sshd hardening
vi /etc/sshd/sshd_config
  PermitRootLogin no
  PasswordAuthentication no
  MaxAuthTries 3
  AllowUsers ryan
  Protocol 2
systemctl restart sshd

# FIPS 140-2/140-3 mode (RHEL 9)
fips-mode-setup --enable
# Requires reboot; changes kernel args and crypto policy
update-crypto-policies --set FIPS
```

---

## Key RHEL Log Locations

| Log / Source | View with |
|-------------|-----------|
| systemd journal | `journalctl -xe` |
| `/var/log/messages` | Traditional syslog (RHEL 7); less used in 8/9 |
| `/var/log/secure` | SSH, sudo, PAM auth events |
| `/var/log/dnf.log` | Package install/remove history |
| `/var/log/audit/audit.log` | SELinux and auditd |
| `/var/log/boot.log` | Boot messages |
| `dmesg` + `/var/log/dmesg` | Kernel ring buffer |
| `/var/crash/` | kdump vmcore files |

---

## LINUX_RHEL_KNOWLEDGE

> Append discoveries here. Format: `YYYY-MM-DD: <note>`
