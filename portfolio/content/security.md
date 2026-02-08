# Security

## Background

Security isn't something I learned on the side - it's where I started my career. I worked at Ernst & Young as a security analyst, conducting VAPT across web, Android, and iOS applications. I reviewed secure configurations of network devices and supported DDoS testing of load balancers to harden client infrastructure.

That experience shapes how I write code today. I think about attack vectors when designing systems. Security isn't an afterthought for me - it's a foundation.

## Current Work

I now work on an External Attack Surface Management and Continuous Automated Red Teaming platform at FireCompass. We scan over a million IPs daily, running reconnaissance, OSINT gathering, and vulnerability scans. I've integrated over 50 security tools into our platform, including Nmap, Nessus, Burp Scanner, and many others.

### What I've Built

**Burp Scanner Integration**: I integrated Burp Scanner into our platform. Multiple Burp instances run on separate VMs, and multiple pods with autoscaling handle scan requests. Any pod can pick up a request and assign it to a Burp instance. Since pods run on spot nodes that can be terminated, I designed a checkpointing system. I regularly fetch partial scan results and save them to cloud storage along with the scan ID and which Burp instance is handling the scan. If a pod goes down, a new pod can pick up the scan ID, download the checkpoint, and route the request back to the same Burp instance to resume from where it left off.

**CVE Matching System**: I enhanced a Day 1 CVE system that matches CVE data with affected assets in OpenSearch. When a new CVE is published, we can quickly identify which of our clients' assets might be affected.

**Graceful Scan Abortion**: I engineered a system to manage and gracefully abort concurrent security scans by integrating with Google Pub/Sub for real-time abort signals. This ensures minimal impact on client networks and prevents unnecessary traffic.

## Security Tools I Work With

| Category | Tools |
|----------|-------|
| **Network Scanning** | Nmap, Masscan |
| **Vulnerability Scanning** | Nessus, Burp Suite, Nuclei |
| **OSINT** | Various reconnaissance tools |
| **Analysis** | Wireshark, Metasploit |

## Security Practices

### In My Code
- Input validation at system boundaries
- Parameterized queries to prevent SQL injection
- Proper authentication and authorization checks
- Secrets management (never in code)
- Dependency auditing

### At Previous Companies
At VuNet Systems, I collaborated with security audit teams to resolve vulnerabilities. Our clients were banks, so security requirements were strict and audits happened for every client. I volunteered to be the SPOC for all security audits because I had a security background and wanted to help strengthen the product.

I conducted sessions for developers to address gaps in our codebase. We cut common vulnerabilities by around 90%. When I left, the product was in a much better security posture than when I joined - that's something I'm proud of.

