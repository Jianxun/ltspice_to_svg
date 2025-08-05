# Security Policy

## Supported Versions

We actively support the following versions of ltspice_to_svg with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| 0.1.x   | :x:                |

## Reporting a Vulnerability

The ltspice_to_svg team takes security bugs seriously. We appreciate your efforts to responsibly disclose your findings, and will make every effort to acknowledge your contributions.

### How to Report Security Issues

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them by email to:

- **Email**: zhujianxun.bupt@gmail.com
- **Subject**: [SECURITY] ltspice_to_svg vulnerability report

Please include the following information in your report:

- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit the issue

This information will help us triage your report more quickly.

### Response Timeline

- **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours.
- **Initial Assessment**: We will provide an initial assessment within 5 business days.
- **Status Updates**: We will send status updates every week until the issue is resolved.
- **Resolution**: We aim to resolve critical vulnerabilities within 30 days.

### What to Expect

After you submit a report, here's what happens:

1. **Confirmation**: We'll confirm the vulnerability and determine its severity.
2. **Fix Development**: We'll work on a fix and prepare a security advisory.
3. **Release**: We'll release a patched version and publish the security advisory.
4. **Credit**: We'll credit you in the security advisory (unless you prefer to remain anonymous).

### Security Update Process

When we release security updates:

- We'll publish a security advisory on GitHub
- We'll update the CHANGELOG.md with security fix details
- We'll release a new version with the fix
- We'll notify users through our release channels

### Safe Harbor

We consider security research conducted under this policy to be:

- Authorized concerning the Computer Fraud and Abuse Act
- Authorized concerning the DMCA (and not a circumvention of technology controls)
- Authorized concerning relevant computer crime laws
- Legitimate research

### Comments on This Policy

If you have suggestions on how this process could be improved, please submit a pull request or file an issue.

---

**Note**: This project is a file format conversion tool that processes local files. While we take security seriously, the attack surface is generally limited to malformed input files that could potentially cause crashes or unexpected behavior.