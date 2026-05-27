---
name: digitalocean
description: DigitalOcean infrastructure — Droplets, managed databases, Spaces, load balancers, firewalls, DNS management
version: 1.0.0
author: veekunth217
tags: [digitalocean, droplet, spaces, managed-database, load-balancer, firewall, dns, doctl]
platforms: [claude-code, cursor, codex]
---

# DigitalOcean Skill

Full DigitalOcean infrastructure management — from Droplet provisioning to managed databases, Spaces, and DNS.

**RULE: Show plan (resources to be created, estimated cost) before provisioning. Wait for GO.**

> **🚧 Status: Stub — implementation pending**
>
> This reference skill has the structure but the snippet content is still being filled in
> (you'll see `<!-- TODO -->` placeholders below). It activates and tells Claude the topic
> exists, but won't yield deep snippets yet.
>
> **Want to help?** Pick any TODO, write the snippet, open a PR. See [CONTRIBUTING.md](../../CONTRIBUTING.md).
> Each contribution moves the skill closer to "Ready" status.

---

## Capabilities

### Droplet Provisioning
<!-- TODO: doctl droplet create, cloud-init user-data, SSH key injection -->
<!-- TODO: Droplet sizing guide (s-1vcpu-1gb through c-32 compute) -->
<!-- TODO: Private networking, reserved IPs, backups, monitoring -->

### Managed Databases
<!-- TODO: PostgreSQL, MySQL, Redis, MongoDB, Kafka clusters -->
<!-- TODO: Connection pooling (PgBouncer), standby nodes, read replicas -->
<!-- TODO: Firewall rules, trusted sources, connection string retrieval -->
<!-- TODO: Automated backups, point-in-time restore -->

### Spaces (S3-Compatible)
<!-- TODO: Bucket creation, CDN endpoint, CORS config -->
<!-- TODO: Access keys, public/private objects, lifecycle rules -->
<!-- TODO: AWS CLI / s3cmd with Spaces endpoint -->
<!-- TODO: Static site hosting via Spaces -->

### Load Balancers
<!-- TODO: HTTP/HTTPS load balancer, health checks -->
<!-- TODO: SSL termination at LB, sticky sessions -->
<!-- TODO: Forwarding rules, backend Droplet targeting -->

### Firewalls
<!-- TODO: Cloud firewall rules (inbound/outbound) -->
<!-- TODO: Apply to Droplet tags (group-based), not just individual droplets -->
<!-- TODO: Common rulesets: web server, database, internal-only -->

### DNS Management
<!-- TODO: Domain import, A/AAAA/CNAME/MX/TXT records -->
<!-- TODO: TTL management, delegation from registrar to DO nameservers -->
<!-- TODO: Wildcard records, CAA records for SSL -->

---

## doctl Quick Reference

```bash
# Auth
doctl auth init

# Droplets
doctl compute droplet list
doctl compute droplet create [name] \
  --size s-2vcpu-4gb \
  --image ubuntu-24-04-x64 \
  --region blr1 \
  --ssh-keys [key-fingerprint] \
  --user-data-file cloud-init.yml

# Databases
doctl databases list
doctl databases connection [db-id] --user doadmin

# Spaces
doctl compute cdn list
# Use AWS CLI with DO endpoint:
aws s3 ls s3://[bucket] \
  --endpoint=https://[region].digitaloceanspaces.com

# DNS
doctl compute domain list
doctl compute domain records list [domain]
doctl compute domain records create [domain] \
  --record-type A --record-name @ --record-data [ip] --record-ttl 300
```

### Terraform for DigitalOcean
```hcl
terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_droplet" "web" {
  name     = "[app]-web"
  size     = "s-2vcpu-4gb"
  image    = "ubuntu-24-04-x64"
  region   = "blr1"
  ssh_keys = [data.digitalocean_ssh_key.default.id]
  tags     = ["web", "[app]"]
}

resource "digitalocean_firewall" "web" {
  name    = "[app]-firewall"
  droplet_ids = [digitalocean_droplet.web.id]

  inbound_rule {
    protocol = "tcp"; port_range = "22"
    source_addresses = ["0.0.0.0/0"]
  }
  inbound_rule {
    protocol = "tcp"; port_range = "80"
    source_addresses = ["0.0.0.0/0"]
  }
  inbound_rule {
    protocol = "tcp"; port_range = "443"
    source_addresses = ["0.0.0.0/0"]
  }
  outbound_rule {
    protocol = "tcp"; port_range = "all"
    destination_addresses = ["0.0.0.0/0"]
  }
}
```

<!-- TODO: Add full interactive workflows for each capability above -->
