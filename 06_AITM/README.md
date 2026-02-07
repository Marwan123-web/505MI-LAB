# 🛡️ AITM Lab 1: HSTS vs SSLStrip Attack Analysis

**Author:** Marwan  
**Course:** Cybersecurity Lab - AITM (Advanced IT Security Management)  
**Academic Year:** 2025/2026  
**Submission:** `06_AITM_1`  
**Date:** January 31, 2026

---

## 📋 Lab Objectives

Demonstrate **HTTP Strict Transport Security (HSTS)** protection against **SSLStrip** MITM attacks:

| Case | Target | HSTS | Result |
|------|--------|------|--------|
| **A** | `example.com` | ❌ None | **Attack Succeeds** |
| **B** | `secure.com` | ✅ Enabled | **Attack Blocked** |

---

## 🔍 Pre-Attack Verification (Terminal)

**HSTS Header Analysis:**
![Terminal Headers](1.png)
![Terminal Headers](2.png)

**Results:**
example.com → ❌ No Strict-Transport-Security
secure.com → ✅ Strict-Transport-Security: max-age=31536000

---

## ⚙️ Burp Suite SSLStrip Configuration

![Burp SSLStrip Config](3.png)

**Critical Settings:**
- ✅ Use TLS for upstream connections
- ❌ No forced HTTPS redirection
- Proxy: `127.0.0.1:8080`

---

## 🚨 Case A: SSLStrip Attack SUCCESS (example.com)

### 1. Intercepted Original Response

![Burp Intercept Original](4.png)

### 2. HTML Modification (MITM Attack)

**Changed:** `"Example Domain"` → `"example.com HACKED BY SSLSTRIP"`

![Burp Modified HTML](5.png)

### 3. Attack Result in Browser

![Hacked Page Loads](6.png)
![Hacked Page Loads](7.png)
**Browser shows:**
- `http://` address bar (unencrypted)
- **No security warnings**

---

## 🔒 Case B: HSTS Protection (secure.com)

### 1. Browser HSTS Cache

chrome://net-internals/#hsts → www.secure.com ✓ ENABLED



![HSTS Cache Proof](13.png)

### 2. HTTP Access Attempt BLOCKED

**Browser auto-upgrades** `http://wwww.secure.com` → `https://www.secure.com`

![Auto HTTPS Upgrade](14.png)

### 1. Browser HSTS Cache
chrome://net-internals/#hsts → www.secure.com ✓ DISABLED



![HSTS Cache Proof](15.png)

### 2. HTTP Access Attempt PASSED

**Browser auto-upgrades** `http://wwww.secure.com` → `http://www.secure.com`

![Auto HTTPS Upgrade](16.png)


---

## 📊 HTTP History Comparison (Burp)

![Traffic Analysis](12.png)

---
### Security Impact

**Without HSTS:** Complete MITM - malware injection possible  
**With HSTS:** Browser-level protection defeats SSLStrip automatically

---