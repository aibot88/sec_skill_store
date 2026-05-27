---
name: wordpress-server
description: WordPress server optimization — Nginx config, PHP 8.3-FPM tuning, Redis object caching, WP Rocket, security hardening, staging, multisite
version: 1.0.0
author: veekunth217
tags: [wordpress, nginx, php-fpm, redis, object-cache, wp-rocket, security, staging, multisite, hardening]
platforms: [claude-code, cursor, codex]
---

# WordPress Server Skill

Production-grade WordPress server configuration — performance, security, caching, and multisite.

**RULE: Show all config changes before applying. Backup reminder before any PHP/Nginx change.**

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

### Nginx + WordPress Config
<!-- TODO: WordPress-specific Nginx server block (try_files, PHP-FPM socket) -->
<!-- TODO: Cache headers for WP Rocket / W3TC static files -->
<!-- TODO: Block xmlrpc.php, block wp-login.php by IP -->
<!-- TODO: WooCommerce cart/checkout bypass for page cache -->

### PHP 8.3-FPM Optimization
<!-- TODO: Pool sizing for WordPress (pm = ondemand for low traffic, dynamic for high) -->
<!-- TODO: opcache.memory_consumption, opcache.max_accelerated_files for WP -->
<!-- TODO: realpath_cache_size, upload_max_filesize, max_execution_time -->
<!-- TODO: PHP slow log setup to catch slow plugins -->

### Redis Object Caching
<!-- TODO: redis-cache plugin setup, wp-config.php constants -->
<!-- TODO: Redis maxmemory-policy for WP (allkeys-lru) -->
<!-- TODO: WooCommerce session handler in Redis -->
<!-- TODO: Cache flushing strategy (selective vs full) -->

### WP Rocket Configuration
<!-- TODO: Page cache, browser cache, minify CSS/JS settings -->
<!-- TODO: CDN integration (DO Spaces / CloudFront) -->
<!-- TODO: WooCommerce-safe cache exclusions -->
<!-- TODO: Preloading, heartbeat control, LazyLoad -->

### Security Hardening
<!-- TODO: Disable file editing in WP admin (DISALLOW_FILE_EDIT) -->
<!-- TODO: Limit login attempts (plugin vs nginx rate limit) -->
<!-- TODO: wp-config.php above webroot -->
<!-- TODO: Database prefix change, user enumeration prevention -->
<!-- TODO: Wordfence / Security plugins vs WAF -->

### Staging Environment Setup
<!-- TODO: Subdomain staging (staging.domain.com), WP CLI duplication -->
<!-- TODO: WP Staging plugin vs manual rsync+dump approach -->
<!-- TODO: Prevent staging from being indexed (robots.txt, noindex) -->
<!-- TODO: Sync staging → prod workflow -->

### Multisite Setup
<!-- TODO: Subdomain vs subdirectory multisite config -->
<!-- TODO: Nginx config for multisite (wildcard subdomains) -->
<!-- TODO: Network admin, per-site plugins vs network-activated -->
<!-- TODO: Domain mapping plugin setup -->

---

## Key wp-config.php Constants

```php
// Performance
define( 'WP_CACHE', true );
define( 'WP_MEMORY_LIMIT', '256M' );
define( 'WP_MAX_MEMORY_LIMIT', '512M' );

// Security
define( 'DISALLOW_FILE_EDIT', true );
define( 'DISALLOW_FILE_MODS', true ); // disable plugin/theme install
define( 'FORCE_SSL_ADMIN', true );

// Redis Object Cache
define( 'WP_REDIS_HOST', '127.0.0.1' );
define( 'WP_REDIS_PORT', 6379 );
define( 'WP_REDIS_DATABASE', 0 );
define( 'WP_REDIS_PREFIX', '[site-key]:' );

// Debug (disable in production)
define( 'WP_DEBUG', false );
define( 'WP_DEBUG_LOG', false );
define( 'SCRIPT_DEBUG', false );
```

### Redis config for WordPress
```conf
# /etc/redis/redis.conf additions
maxmemory 256mb
maxmemory-policy allkeys-lru
save ""                        # disable RDB persistence for cache-only use
appendonly no
```

<!-- TODO: Add full interactive workflows for each capability above -->
