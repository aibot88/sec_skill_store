---
name: noc
description: >
  Expert network operations and censorship circumvention skill. Use for ANY networking
  question: TCP/IP internals, routing, DNS, firewalls, iptables/nftables, Linux networking,
  Wireshark/tcpdump analysis, VPN protocols (WireGuard, AmneziaWG 1.5, VLESS+Reality,
  Hysteria2, Shadowsocks, MTProxy), DPI evasion, traffic obfuscation, censorship bypass
  (ТСПУ РФ, whitelist режим, GFW, SNI filtering, IP blocking), self-hosted VPN
  infrastructure (3x-ui, Xray, Amnezia), whitelist bypass через YC/VK Cloud IP,
  zapret/zapret2/b4, VK TURN proxy, MTU/latency debugging, domain lists (itdoginfo),
  Prometheus monitoring of VPN nodes (whitebox). Trigger on: "не работает интернет",
  "обход блокировки", "белые списки", "ТСПУ", paste любых ip/ss/tc/nftables вывода,
  VPN конфиги, Wireshark дампы, routing tables, или любой вопрос про сети и цензуру.
  Всегда читай references/dpi-censorship.md когда вопрос про блокировки в РФ —
  там аналитический фреймворк и актуальные инструменты.
---

# Networking Skill

## Identity & Style

Senior network engineer + практик обхода цензуры. Отвечаю на русском, кратко и по делу.
Адаптивный стиль: команда → сразу команда; "как работает" → объяснение с деталями.

---

## Диагностика — быстрый чеклист

### Базовая связность
```bash
# L3 — доступность
ping -c4 -W1 <host>
traceroute -n <host>          # или mtr --report --no-dns <host>
mtr -n --report-cycles 20 <host>

# DNS
dig +short <domain>
dig +trace <domain>           # полная цепочка резолвинга
resolvectl query <domain>     # systemd-resolved
nslookup <domain> 8.8.8.8    # через конкретный резолвер

# L4 — порт открыт?
nc -zv <host> <port>
telnet <host> <port>
curl -v --connect-timeout 5 https://<host>
```

### Интерфейсы и маршруты
```bash
ip addr show
ip link show
ip route show
ip route show table all       # все таблицы маршрутизации
ip rule list                  # policy routing rules

# Конкретный маршрут до хоста
ip route get <destination>

# ARP / соседи
ip neigh show
arp -n
```

### Активные соединения
```bash
ss -tunap                     # все TCP/UDP с процессами
ss -tunap state established   # только установленные
ss -tlnp                      # listening TCP
netstat -rn                   # таблица маршрутов (старый способ)

# Трафик в реальном времени
iftop -n -i eth0
nethogs eth0                  # по процессам
nload eth0
```

### Пакеты — захват
```bash
# Базовый захват
tcpdump -i eth0 -nn host <ip>
tcpdump -i eth0 -nn port 443
tcpdump -i any -nn -w /tmp/capture.pcap

# Только SYN пакеты (новые соединения)
tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'

# DNS запросы
tcpdump -i eth0 -nn udp port 53

# Размер пакетов (для MTU диагностики)
tcpdump -i eth0 -nn -v host <ip> | grep length
```

---

## Linux Networking — iptables / nftables

### iptables — частые операции
```bash
# Просмотр правил с номерами
iptables -L -n -v --line-numbers
iptables -t nat -L -n -v

# Добавить правило
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -I INPUT 1 -s <ip> -j DROP   # вставить первым

# NAT (masquerade для VPN)
iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o eth0 -j MASQUERADE

# Сохранить / восстановить
iptables-save > /etc/iptables/rules.v4
iptables-restore < /etc/iptables/rules.v4
```

### nftables
```bash
nft list ruleset
nft list table inet filter

# Базовый файрвол
nft add table inet filter
nft add chain inet filter input { type filter hook input priority 0 \; policy drop \; }
nft add rule inet filter input ct state established,related accept
nft add rule inet filter input tcp dport { 22, 80, 443 } accept
```

### IP forwarding (нужен для VPN/роутинга)
```bash
sysctl net.ipv4.ip_forward                    # проверить
sysctl -w net.ipv4.ip_forward=1               # включить сейчас
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.d/99-forward.conf  # постоянно
```

---

## MTU / MSS — частая причина проблем

```bash
# Определить MTU на пути (Path MTU Discovery)
ping -M do -s 1472 <host>     # 1472 + 28 = 1500 (стандартный MTU)
ping -M do -s 1400 <host>     # уменьшай пока не пройдёт

# Для VPN интерфейсов обычно:
# WireGuard: MTU 1420 (1500 - 80 overhead)
# WireGuard поверх WireGuard: MTU 1380

# Принудительно установить MTU
ip link set dev wg0 mtu 1380

# MSS clamping (фикс для TCP через VPN)
iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN \
  -j TCPMSS --clamp-mss-to-pmtu
```

---

## WireGuard — базовые операции

```bash
# Статус
wg show
wg show wg0 latest-handshakes

# Генерация ключей
wg genkey | tee privatekey | wg pubkey > publickey
wg genpsk > presharedkey     # опционально, усиливает безопасность

# Добавить peer на лету (без перезапуска)
wg set wg0 peer <pubkey> allowed-ips 10.0.0.2/32 endpoint <ip>:<port>

# Диагностика
ip route show table all | grep wg0
wg show wg0 transfer          # байты sent/received
```

### wg0.conf — шаблон сервера
```ini
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <server-private-key>
PostUp   = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey  = <client-public-key>
AllowedIPs = 10.0.0.2/32
PresharedKey = <psk>          # опционально
```

---

## Сети и подсети — быстрый расчёт

```bash
# ipcalc — удобно
ipcalc 192.168.1.0/24
ipcalc 10.0.0.0/8 --split 4  # разбить на подсети

# sipcalc — детально
sipcalc 192.168.1.128/26
```

| CIDR | Хостов | Маска |
|------|--------|-------|
| /24  | 254    | 255.255.255.0 |
| /25  | 126    | 255.255.255.128 |
| /26  | 62     | 255.255.255.192 |
| /27  | 30     | 255.255.255.224 |
| /28  | 14     | 255.255.255.240 |
| /30  | 2      | 255.255.255.252 |

---

## Reference Files

- `references/vpn-protocols.md` — AmneziaWG, Hysteria2, VLESS+Reality, Shadowsocks, сравнение
- `references/dpi-censorship.md` — ТСПУ, методы блокировок, обход: zapret, nfqws, tpws
- `references/wireshark.md` — фильтры, анализ VPN трафика, детектирование DPI