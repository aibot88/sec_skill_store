---
name: eresus-php-audit
description: >
  Deep PHP-specific security audit skill covering injection, deserialization, file operations,
  auth bypass, POP chain discovery, and CMS-specific patterns.
  Trigger when auditing PHP code: "audit this PHP app", "find PHP security issues",
  "check Laravel/WordPress for vulnerabilities", "PHP SAST review",
  "check for PHP deserialization", "review this WordPress plugin".
  Includes scripts/rules.json for programmatic rule lookup.
metadata:
  version: "1.0"
  domain: application-security
  mode: php-audit
  persona: php-security-researcher
---

# PHP Security Audit

## Purpose

Perform a comprehensive, depth-first security audit of PHP codebases.
This skill provides the complete knowledge of Kunlun-M's CVI rule set,
organized by vulnerability class, plus framework-specific patterns for
Laravel, WordPress, Symfony, and modern PHP 8.x applications.

Use `view_file` and `grep_search` exclusively. No terminal commands.

---

## Audit Workflow

### Phase 1: Reconnaissance

1. Identify the PHP framework/CMS (Laravel, WordPress, Symfony, CodeIgniter, raw PHP)
2. Check `composer.json` / `composer.lock` for known vulnerable dependencies
3. Map entry points: routes, controllers, REST endpoints, admin pages, AJAX handlers
4. Identify the autoloader and class loading mechanism
5. Check PHP version requirements (`php` constraint in `composer.json`)

### Phase 2: Entry Point Discovery

Inspired by Kunlun-M's EntranceFinder plugin — systematically find all user-facing entry points:

1. **Direct file access** — find all `.php` files that can be accessed directly (not included/required)
2. **Route definitions** — check framework routing files
3. **AJAX handlers** — WordPress `wp_ajax_*`, Laravel API routes, custom handlers
4. **CLI entry** — Artisan commands, WP-CLI commands, custom scripts
5. **Cron jobs** — scheduled tasks that process external data

Search patterns for entry points:
- Files with `$_GET`, `$_POST`, `$_REQUEST`, `$_FILES`, `$_COOKIE`, `$_SERVER`
- Files with `file_get_contents('php://input')`
- Laravel: `Route::get`, `Route::post`, `Route::any`, `Route::resource`
- WordPress: `add_action('wp_ajax_`, `add_action('rest_api_init`
- Symfony: `#[Route(`, `@Route(`, `routing.yaml` definitions

---

## CVI Rules — Injection

### CVI-1001: SSRF
Search for HTTP request functions with user-controlled URLs:

```
curl_setopt($ch, CURLOPT_URL, $userInput)
file_get_contents($userUrl)
fopen($userUrl, 'r')
$client->get($userInput)  // Guzzle
$client->request('GET', $userInput)
```

**Severity**: HIGH — can lead to internal service access, cloud metadata theft
**Trace**: Check if URL comes from `$_GET`, `$_POST`, database with user data

### CVI-1002: SQL Injection
Search for raw SQL construction:

```
$db->query("SELECT * FROM users WHERE id = " . $_GET['id'])
$wpdb->query("SELECT * FROM $table WHERE id = $id")
$pdo->query("SELECT ... $var ...")
mysqli_query($conn, "... $var ...")
```

**Safe patterns**: `$pdo->prepare()`, `$wpdb->prepare()`, Eloquent query builder
**Severity**: CRITICAL when user input reaches query without parameterization

### CVI-1003: Command Injection
Search for shell execution functions:

```
system($userInput)
exec($userInput)
passthru($userInput)
shell_exec($userInput)
`$userInput`  (backticks)
popen($userInput, 'r')
proc_open($userInput, ...)
pcntl_exec($userInput)
```

**Severity**: CRITICAL — always results in RCE if input is user-controlled

### CVI-1004: Code Injection
Search for dynamic code execution:

```
eval($userInput)
assert($userInput)  // PHP < 8.0
preg_replace('/.*/e', $replacement, $subject)  // deprecated /e modifier
create_function($args, $userInput)
call_user_func($userInput, $args)
call_user_func_array($userInput, $args)
array_map($userInput, $data)
usort($data, $userInput)
```

**Severity**: CRITICAL if any argument is user-controlled

### CVI-1005: XSS
Search for unescaped output:

```
echo $_GET['input']
echo $userInput   // without htmlspecialchars()
<?= $userInput ?>
print($userInput)
printf("%s", $userInput)  // in HTML context
```

**Safe patterns**: `htmlspecialchars($var, ENT_QUOTES, 'UTF-8')`, `esc_html()` (WP), `{{ $var }}` (Blade)
**Dangerous**: `{!! $var !!}` (Laravel Blade raw), `| raw` (Twig)

### CVI-1006: File Inclusion (LFI/RFI)

```
include($userInput)
include_once($userInput)
require($userInput)
require_once($userInput)
```

**Severity**: CRITICAL if path is user-controlled
**Check**: Is `allow_url_include` enabled? (RFI)

### CVI-1007: File Operations

```
file_get_contents($userInput)     // path traversal read
file_put_contents($userInput, $data)  // arbitrary file write
unlink($userInput)                // arbitrary file delete
copy($src, $userInput)            // arbitrary file placement
rename($old, $userInput)          // arbitrary file move
readfile($userInput)              // information disclosure
```

**Severity**: HIGH to CRITICAL depending on operation

### CVI-1008: XML External Entity (XXE)

```
$doc = new DOMDocument()
$doc->loadXML($userInput)              // XXE if no protection
simplexml_load_string($userInput)       // XXE
$reader = new XMLReader()
$reader->xml($userInput)               // XXE
```

**Safe**: `libxml_disable_entity_loader(true)` (deprecated PHP 8.0+, secure by default)

---

## CVI Rules — Deserialization

### CVI-2001: PHP Object Injection

```
unserialize($userInput)
unserialize($_COOKIE['data'])
unserialize(base64_decode($_GET['data']))
```

**Severity**: CRITICAL — Property-Oriented Programming (POP) chain exploitation
**Gadget hunting**: Search for classes with:
- `__wakeup()` — called on deserialization
- `__destruct()` — called on object destruction
- `__toString()` — called on string cast
- `__call()` — called on undefined method
- `__get()` / `__set()` — called on property access

### CVI-2002: PHP Unserialize Chain Discovery

Kunlun-M's `phpunserializechain` plugin methodology — trace POP chains:

1. **Find the entry sink**: `unserialize()` with user input
2. **Find gadget classes**: Classes with magic methods that perform I/O
3. **Trace the chain**: `__destruct()` → calls method → file write / command exec
4. **Popular chains**: 
   - Laravel: `PendingBroadcast` → `__destruct()` → `dispatch()`
   - Symfony: `Process` → `__destruct()` → `stop()` → command execution
   - WordPress: Various plugin-specific chains
   - Monolog: `BufferHandler` → `__destruct()` → `close()` → arbitrary write

---

## CVI Rules — Authentication & Authorization

### CVI-3001: Authentication Bypass

```
// Weak comparison
if ($_POST['password'] == $storedPassword)  // type juggling: "0" == 0
if (md5($_POST['password']) == $storedHash)  // magic hash: "0e..." == 0

// Missing auth check
// Check if sensitive functions lack is_admin(), current_user_can(), auth check
```

**Key pattern**: `==` vs `===` for authentication — PHP type juggling attack

### CVI-3002: Session & Cookie Security

```
session_set_cookie_params(['secure' => false])
setcookie($name, $value)  // missing secure, httponly, samesite flags
$_SESSION['admin'] = $_POST['is_admin']  // user-controlled session data
session_id($_GET['sessid'])  // session fixation
```

### CVI-3003: CSRF

```
// Missing CSRF token verification
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // No token check before processing
}

// WordPress: Missing nonce verification
// check_ajax_referer() missing
// wp_verify_nonce() missing
```

---

## CVI Rules — Configuration & Information Disclosure

### CVI-4001: Information Disclosure

```
phpinfo()
error_reporting(E_ALL)
display_errors = On
var_dump($sensitiveData)
print_r($debug)
```

### CVI-4002: Hardcoded Secrets

```
$password = "hardcoded"
$apiKey = "sk_live_..."
$dbPassword = "root"
define('DB_PASSWORD', 'actual_password')
```

### CVI-4003: Dangerous PHP Configuration

```
allow_url_fopen = On      // enables RFI via include()
allow_url_include = On    // enables remote file inclusion
expose_php = On           // version disclosure
register_globals = On     // variable injection (legacy)
magic_quotes_gpc = Off    // no auto-escaping (legacy)
open_basedir               // check if properly set
disable_functions          // check if dangerous funcs are disabled
```

---

## Framework-Specific Deep Checks

### Laravel
- Check `.env` file exposure (web-accessible `.env`)
- Check `APP_DEBUG=true` in production
- Check `APP_KEY` rotation
- Check for `{!! !!}` raw Blade output with user data
- Check Eloquent mass assignment: `$fillable` vs `$guarded`
- Check Gate/Policy authorization on controllers
- Check `Route::any()` over-permissive routing
- Check file upload handling: stored path, extension validation
- Check queue job deserialization (jobs are serialized/unserialized)

### WordPress
- Check for direct file access without `defined('ABSPATH')` check
- Check `$wpdb->prepare()` usage (must use %s, %d placeholders)
- Check `update_option()` / `add_option()` with user input
- Check `wp_remote_get()` / `wp_remote_post()` for SSRF
- Check `is_admin()` (checks admin page, NOT admin privilege — use `current_user_can()`)
- Check nonce verification on all form handlers
- Check `esc_html()`, `esc_attr()`, `esc_url()`, `wp_kses()` usage
- Check REST API permission callbacks (`permission_callback` must not be `__return_true` for sensitive data)
- Check `sanitize_text_field()`, `absint()`, `wp_unslash()` input sanitization

### Symfony
- Check `@Route` with missing security annotations
- Check Twig `| raw` filter with user data
- Check `kernel.debug` in production
- Check voter/access decision manager configuration
- Check CSRF token service usage

---

## Supply Chain Checks

### Composer Dependencies
- Check `composer.lock` for known CVEs (compare against advisories)
- Check for abandoned packages
- Check for packages with `eval()`, `system()`, `exec()` in install scripts
- Check post-install/post-update scripts in `composer.json`

---

## Red Flags Checklist

- [ ] Any use of `unserialize()` with external data
- [ ] Any use of `eval()`, `assert()`, `create_function()`
- [ ] `==` comparison for authentication/authorization
- [ ] `$_GET`/`$_POST` directly in SQL queries
- [ ] `$_GET`/`$_POST` in `include()`/`require()`
- [ ] File operations with user-controlled paths
- [ ] `echo`/`print` of user input without encoding
- [ ] Missing CSRF token verification on state-changing actions
- [ ] `APP_DEBUG=true` or `display_errors=On` in production
- [ ] Hardcoded credentials in source code
- [ ] `allow_url_include` enabled
- [ ] WordPress: `is_admin()` used for privilege checks (wrong function)
- [ ] Laravel: `{!! $userInput !!}` in Blade templates

---

## Report Format

For each finding, report:

```
### CVI-[ID]: [Vulnerability Class]

**Severity**: [LOW/MEDIUM/HIGH/CRITICAL]
**Confidence**: [LOW/MEDIUM/HIGH]
**File**: [path]:[line]

**Vulnerable Code**:
[show the code]

**Data Flow**:
[source] → [intermediaries] → [sink]

**Impact**: [what an attacker achieves]
**Remediation**: [specific fix with code example]
**CVI Reference**: CVI-[xxxx]
```

---

## Tooling Constraints

Use ONLY:
- `view_file` — read source code
- `grep_search` — find patterns across the codebase

Do NOT use any terminal commands.
