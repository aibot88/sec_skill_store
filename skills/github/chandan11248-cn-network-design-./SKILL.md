# CN Mini-Project Skill Guide -- Market Network Domain

> A step-by-step guide to designing and implementing a Computer Networks mini-project
> using a Market / Shopping Complex as the real-world scenario.
> Follows the same requirements as the IOE Pulchowk CN (CT 654) course project.

---

## Scenario: Fishtail Market Network

A multi-storey shopping complex with the following wings/departments:

| Wing / Department          | Real-World Function                                      |
|----------------------------|----------------------------------------------------------|
| Management Office          | Admin, HR, accounts, billing, security control room      |
| Retail Floor A             | Clothing, electronics, accessories shops                 |
| Retail Floor B             | Groceries, household goods, supermarket                  |
| Food Court                 | Restaurants, cafes, fast-food counters                   |
| Warehouse & Logistics      | Inventory storage, loading docks, delivery management    |
| Customer Services          | Help desk, loyalty program kiosk, returns counter        |
| IT & Server Room           | POS server, inventory DB, CCTV NVR, backup systems      |

---

## Step 1: Requirements Checklist

Make sure your design satisfies ALL these requirements:

| #  | Requirement                              | Minimum                                      |
|----|------------------------------------------|-----------------------------------------------|
| 1  | IP address block                         | >= /22 (1024 addresses)                       |
| 2  | LAN networks                             | >= 9 networks, >= 6 different subnet sizes    |
| 3  | VLANs spanning multiple switches         | >= 3 VLANs, each across >= 3 switches         |
| 4  | Routers                                  | >= 9 routers, at least 3 without a LAN        |
| 5  | OSPF areas                               | >= 3 areas (including backbone Area 0)        |
| 6  | Static route to ISP                      | No dynamic routing with ISP                   |
| 7  | DNS servers                              | >= 2 internal DNS + 1 ISP DNS                 |
| 8  | Web servers                              | >= 2 web servers on different subnets          |
| 9  | DHCP servers                             | At least 1 (more recommended per wing)        |
| 10 | Multiple paths / redundancy              | >= 2 networks with redundant paths            |

---

## Step 2: Choose Your IP Block

Use a private /22 block. Example:

    Master Block:    10.10.0.0/22
    Address Range:   10.10.0.0 - 10.10.3.255
    Total Addresses: 1024

You can also use 172.16.x.x/22 or 192.168.x.x/22. Just stay consistent.

---

## Step 3: VLSM Subnet Table

### Point-to-Point Links (/30 each, 9 links)

| Link | Connects       | Subnet          |
|------|----------------|-----------------|
| P1   | ISP-R1 - R1    | 10.10.0.0/30    |
| P2   | R1 - R2        | 10.10.0.4/30    |
| P3   | R1 - R3        | 10.10.0.8/30    |
| P4   | R1 - R4        | 10.10.0.12/30   |
| P5   | R4 - R5        | 10.10.0.16/30   |
| P6   | R2 - R6        | 10.10.0.20/30   |
| P7   | R3 - R7        | 10.10.0.24/30   |
| P8   | R5 - R8        | 10.10.0.28/30   |
| P9   | R8 - R9        | 10.10.0.32/30   |

### LAN Subnets (9 networks, 6 sizes)

| #  | Network Name                  | Size | Subnet             | Hosts |
|----|-------------------------------|------|---------------------|-------|
| L1 | Management Office             | /24  | 10.10.1.0/24        | 254   |
| L2 | Customer Services & Help Desk | /25  | 10.10.2.0/25        | 126   |
| L3 | VLAN 10 - Retail Floor A      | /26  | 10.10.3.0/26        | 62    |
| L4 | VLAN 20 - Retail Floor B      | /27  | 10.10.3.64/27       | 30    |
| L5 | VLAN 30 - Food Court          | /27  | 10.10.3.96/27       | 30    |
| L6 | VLAN 40 - IT Server Room      | /28  | 10.10.3.128/28      | 14    |
| L7 | VLAN 60 - Warehouse           | /28  | 10.10.3.144/28      | 14    |
| L8 | VLAN 50 - Security / CCTV     | /27  | 10.10.3.160/27      | 30    |
| L9 | VLAN 70 - Kiosk / POS Network | /29  | 10.10.3.192/29      | 6     |

6 different sizes used: /24, /25, /26, /27, /28, /29

---

## Step 4: VLAN Design

| VLAN ID | Name                  | Switches        | Gateway Router |
|---------|-----------------------|-----------------|----------------|
| 10      | Retail Floor A        | SW3, SW4, SW5   | R3             |
| 20      | Retail Floor B        | SW3, SW4, SW5   | R3             |
| 30      | Food Court            | SW3, SW4, SW5   | R7             |
| 40      | IT Server Room        | SW5             | R9             |
| 50      | Security / CCTV       | SW5             | R9             |
| 60      | Warehouse & Logistics | SW4             | R7             |
| 70      | Kiosk / POS Network   | SW3             | R3             |

- VLANs 10, 20, 30 each span 3 switches (SW3, SW4, SW5) -- satisfies requirement #3
- Inter-VLAN routing via Router-on-a-Stick (sub-interfaces on R3, R7, R9)
- 802.1Q trunking between SW3-SW4-SW5

---

## Step 5: Router & OSPF Design

### Router Roles (10 routers total)

| Router | Role                               | OSPF Area |
|--------|-------------------------------------|-----------|
| R1     | ASBR + ABR (Area 0/1)              | 0, 1      |
| R2     | LAN Router (Management)            | 1         |
| R3     | ABR (Area 0/1)                     | 0, 1      |
| R4     | Transit - no LAN                   | 0         |
| R5     | Transit - no LAN                   | 0         |
| R6     | LAN Router (Customer Services)     | 1         |
| R7     | LAN Router (Warehouse/Food Court)  | 1         |
| R8     | ABR + Transit - no LAN             | 0, 2      |
| R9     | LAN Router (IT/Security)           | 2         |
| ISP-R1 | Edge Router (ISP side)             | -         |

3 routers without LAN: R4, R5, R8
3 OSPF Areas: Area 0 (Backbone), Area 1 (Retail Wing), Area 2 (IT & Security Wing)

### ISP Connection

    R1 -> ISP-R1 via static default route (0.0.0.0/0)
    ISP-R1 -> R1 via static return route (10.10.0.0/22)
    No OSPF with ISP.

---

## Step 6: Servers

| Server Role   | IP Address   | Subnet         | Location                |
|---------------|--------------|----------------|-------------------------|
| DNS Server 1  | 10.10.1.3    | 10.10.1.0/24   | Management Office (SW1) |
| DNS Server 2  | 10.10.3.130  | 10.10.3.128/28 | IT Server Room (SW5)    |
| ISP DNS       | 203.0.113.10 | 203.0.113.0/24 | ISP Network             |
| Web Server 1  | 10.10.2.3    | 10.10.2.0/25   | Customer Services (SW2) |
| Web Server 2  | 10.10.3.131  | 10.10.3.128/28 | IT Server Room (SW5)    |
| DHCP Server 1 | 10.10.1.2    | 10.10.1.0/24   | Management Office (SW1) |
| DHCP Server 2 | 10.10.2.2    | 10.10.2.0/25   | Customer Services (SW2) |
| DHCP Server 3 | 10.10.3.162  | 10.10.3.160/27 | Security Wing (SW5)     |

---

## Step 7: Redundancy / Multiple Paths

1. Retail Wing Redundancy (Area 1):
   - Path A: R1 -> R2 -> R6 (Management / Customer Services)
   - Path B: R1 -> R3 -> R7 (Retail Floors / Warehouse)

2. Backbone Redundancy:
   - R1 -> R4 -> R5 -> R8 provides failover transit
   - OSPF auto-converges on link failure

---

## Step 8: Build in Cisco Packet Tracer

Order of operations:

 1. Place routers - R1 through R9 + ISP-R1 (use 2911 or 1941 routers)
 2. Place switches - SW1 through SW5 (use 2960 switches)
 3. Cable P2P links - Serial DCE/DTE cables between routers (clock rate 64000)
 4. Cable router-to-switch links - GigabitEthernet or FastEthernet
 5. Cable trunk links - SW3 to SW4 to SW5 (set switchport mode trunk)
 6. Configure VLANs on SW3, SW4, SW5
 7. Create sub-interfaces on R3, R7, R9 for inter-VLAN routing (encapsulation dot1Q)
 8. Assign IP addresses to all router interfaces per subnet table
 9. Configure OSPF - process 1, correct area assignments on each interface
10. Configure static routes - default on R1, return route on ISP-R1
11. Set up servers - DNS, Web, DHCP with correct IPs
12. Place PCs - at least 1-2 per LAN, set to DHCP or static
13. Test connectivity - ping across VLANs, areas, and to ISP; test DNS resolution

### Common Packet Tracer commands:

    ! --- VLAN creation on switch ---
    Switch(config)# vlan 10
    Switch(config-vlan)# name RetailFloorA

    ! --- Trunk port ---
    Switch(config-if)# switchport mode trunk
    Switch(config-if)# switchport trunk allowed vlan 10,20,30

    ! --- Access port ---
    Switch(config-if)# switchport mode access
    Switch(config-if)# switchport access vlan 10

    ! --- Router sub-interface (Router-on-a-Stick) ---
    Router(config)# interface GigabitEthernet0/0.10
    Router(config-subif)# encapsulation dot1Q 10
    Router(config-subif)# ip address 10.10.3.1 255.255.255.192

    ! --- OSPF ---
    Router(config)# router ospf 1
    Router(config-router)# network 10.10.3.0 0.0.0.63 area 1

    ! --- Static default route (on R1) ---
    Router(config)# ip route 0.0.0.0 0.0.0.0 10.10.0.1

---

## Step 9: Write the Proposal (LaTeX)

Your proposal document should contain these sections:

1. Title Page - University, course, name, roll number
2. Network Topology - Overview, diagram, key features
3. Description - IP pool, P2P subnet table, LAN subnet table, VLAN table,
   server table, routing spec, redundancy, additional specs
4. Department-to-Network Mapping - Which market department maps to which VLAN/LAN
5. Requirements Compliance - Checklist table showing each requirement is met

### LaTeX tips:
- Use p{Xcm} column types for long table cells to enable text wrapping
- Use \checkmark for the compliance table
- Use float package + [H] to pin tables/figures in place
- Export Packet Tracer topology as screenshot -> convert to PDF for inclusion

---

## Step 10: Diagrams

Create two diagrams:

1. Network Topology Diagram (Figure 1) - All routers, switches, links,
   subnet labels, server icons, and VLAN assignments.

2. OSPF Area Topology Diagram (Figure 2) - Bubble/circle view showing
   Area 0, Area 1, Area 2 with department circles, ABR nodes, and summary box.

---

## Quick Adaptation Guide

To adapt this template to your own domain, replace the department names:

| This Template (Market)  | Hospital Example     | University Example     |
|-------------------------|----------------------|------------------------|
| Management Office       | Administration Wing  | Admin & Registrar      |
| Retail Floor A          | General Ward         | Engineering Block      |
| Retail Floor B          | Private Ward         | Science Block          |
| Food Court              | Maternity Ward       | Library & Media Center |
| Warehouse & Logistics   | Lab & Radiology      | Sports Complex         |
| Customer Services       | OPD                  | Student Affairs        |
| IT & Server Room        | Critical Care / ICU  | Data Center            |
| Kiosk / POS Network     | Pharmacy             | Wi-Fi Hotspot Zone     |
| Security / CCTV         | Emergency Dept.      | Campus Security        |

The network structure stays the same -- only department names and the narrative change.

---

## Deliverables Checklist

- [ ] proposal.tex - Complete LaTeX proposal document
- [ ] network-topology.svg / .pdf - Figure 1 diagram
- [ ] ospf-area-topology.svg / .pdf - Figure 2 diagram
- [ ] subnet-table.txt - VLSM calculations (reference)
- [ ] Cisco Packet Tracer .pkt file - Working simulation
- [ ] Compile and verify PDF renders correctly (no cut-off tables)
- [ ] All 10 requirements satisfied (see Step 1)
