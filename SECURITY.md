# Security Policy

This repository is a fork of the Asimov v1 humanoid robot that carries a safety-assurance record beside the robot's
sources. A security problem in the robot's software can move a 35 kg machine around people, so please report it
privately.

## Reporting a vulnerability

- Use GitHub private vulnerability reporting on this repository: **Security** tab → **Report a vulnerability**
  (or [open a report directly](https://github.com/jherrodthomas/asimov-v1/security/advisories/new)).
- Do not open public issues, pull requests or discussions for security problems.

Please include the affected repository and commit (this fork, or the upstream firmware, API or policy repository
once published), the robot configuration (CFG-001 tethered and bench-powered, or CFG-002 with a battery and the
policy), a description of the issue and its impact, and how you found it. Proof-of-concept material is welcome but
not required. Do not send personal data of other people.

### What to expect

- Acknowledgement within 3 working days.
- Initial assessment within 5 working days (2 if the issue could move the robot, defeat a stop or drop the robot).
- If the issue can affect safety, we may say to stop powering the robot before a fix is ready. Such notices contain
  no technical detail.
- We aim to release a fix and publish an advisory within 90 days, and we coordinate disclosure timing with you. We
  credit reporters who wish to be credited.

### Scope

In scope: this repository (the record, its tools and CI, the fork's changes to the sources), the fork's firmware
safety layer and container builds once they exist, and the fork's update and release process.

Out of scope here: upstream Asimov v1 (Asimov Inc.), the upstream Asimov API, tele-operation app and locomotion
policy, and third-party services. Report those to their owners; if you are unsure, report to us and we will route it.

### Testing rules

Test only on equipment you own or are authorised to test. Never test on a robot with people within reach of a powered
limb, and never with the robot standing free of its tether. Do not access other people's devices, networks or
accounts, and do not attack upstream or third-party infrastructure.

### Supported releases

The fork publishes no release yet. When it does, only the latest release receives security fixes.

The process behind this policy is [WP-O-05](assurance/09-production-operation/WP-O-05-cybersecurity-incident-response-updates.md);
the cybersecurity plan is [WP-M-08](assurance/01-management/WP-M-08-cybersecurity-plan.md).

## Cybersecurity engineering under IEC 62443

Cybersecurity is treated as an engineering discipline alongside machinery safety, not only as vulnerability
intake. The fork follows IEC 62443-4-1 (secure product development lifecycle) and IEC 62443-4-2 (component
requirements) with a security level target decided by the project lead. The known starting position, from the
[gap assessment](assurance/00-assessment/gap-assessment.md): the tele-operation authentication scheme is not
documented (GAP-19), the Asimov API is pre-1.0 and unstable (GAP-18), and the wireless E-stop link and the UART debug
port have no documented protection (GAP-20). Threats that can cause a hazard are rated against the hazard list, and
the hardwired stop chain is designed as a zone with no conduit from the tele-operation network, so that no attack on
the software can hold a contactor closed or command a joint past its clamp.
