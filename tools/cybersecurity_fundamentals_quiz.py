#!/usr/bin/env python3
"""
Cybersecurity Fundamentals Quiz
===============================

A self-contained Tkinter quiz application designed to run on macOS
(and also compatible with Windows/Linux).

Features
--------
• Large embedded cybersecurity question bank
• Key terms and definitions
• Fundamental concepts
• Security scenarios
• Explanation questions
• Matching questions
• Fill-in-the-blank questions
• Category and question-type filters
• Vector-style illustration drawn with Tkinter Canvas for every question
• User must make an attempt before revealing the sample answer
• Random question generation
• Session score/progress for objectively keyed questions

No external files or third-party packages are required.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import re

APP_TITLE = "Cybersecurity Fundamentals Quiz"
WINDOW_SIZE = "1220x820"

QUESTIONS = []

def add(category, qtype, question, answer, explanation, icon="shield",
        choices=None, correct=None, match_items=None, aliases=None):
    QUESTIONS.append({
        "category": category,
        "type": qtype,
        "question": question,
        "answer": answer,
        "explanation": explanation,
        "icon": icon,
        "choices": choices or [],
        "correct": correct,
        "match_items": match_items or [],
        "aliases": aliases or []
    })

# ---------------------------------------------------------------------
# KEY TERMS & DEFINITIONS
# ---------------------------------------------------------------------

terms = [
("CIA triad","Confidentiality, Integrity, and Availability","The three core security objectives: limiting unauthorized disclosure, protecting accuracy/trustworthiness, and keeping systems/data accessible.","shield"),
("confidentiality","Protecting information from unauthorized disclosure","Confidentiality is about preventing people or systems without authorization from viewing sensitive information.","lock"),
("integrity","Protecting data from unauthorized or improper modification","Integrity means information remains accurate, complete, and trustworthy.","shield"),
("availability","Keeping systems and information accessible when needed","Availability is supported by redundancy, backups, resilient infrastructure, and incident response.","server"),
("authentication","Verifying the identity of a user, device, or service","Authentication answers: Who are you?","key"),
("authorization","Determining what an authenticated identity is allowed to access or do","Authorization answers: What are you allowed to do?","key"),
("accounting","Recording and tracking user or system activity","Accounting creates records that support auditing, troubleshooting, and investigations.","log"),
("least privilege","Giving users and systems only the access necessary to perform their duties","Least privilege reduces the impact of mistakes, misuse, and account compromise.","key"),
("defense in depth","Using multiple layers of security controls","If one control fails, other layers can still reduce or contain the risk.","shield"),
("risk","The potential for loss or harm when a threat can exploit a vulnerability","Risk is often prioritized by considering likelihood and impact.","warning"),
("threat","Anything capable of causing harm to an asset","Threats can include attackers, malware, insiders, equipment failure, and natural events.","warning"),
("vulnerability","A weakness that could be exploited","Vulnerabilities can exist in software, hardware, configurations, processes, or human behavior.","bug"),
("exploit","A method or code that takes advantage of a vulnerability","An exploit uses a weakness to create an unintended security effect.","bug"),
("attack surface","All points where an attacker might try to enter, interact with, or extract data from a system","Reducing unnecessary services, ports, accounts, and software can reduce attack surface.","network"),
("asset","Something valuable that an organization needs to protect","Assets can include data, systems, people, facilities, credentials, and reputation.","server"),
("control","A safeguard used to reduce risk","Controls may be administrative, technical, or physical; preventive, detective, or corrective.","shield"),
("security policy","A formal statement of security expectations and requirements","Policies define approved behavior, responsibilities, and organizational rules.","document"),
("standard","A mandatory detailed requirement that supports policy","Standards specify consistent requirements such as encryption strength or password configuration.","document"),
("procedure","Step-by-step instructions for performing a task","Procedures explain how to carry out an activity consistently.","document"),
("guideline","Recommended guidance that allows some flexibility","Guidelines are usually less mandatory than policies and standards.","document"),
("incident","An event that threatens or violates security objectives or policy","Security incidents require appropriate triage, containment, investigation, and recovery.","warning"),
("event","An observable occurrence in a system or network","Not every event is an incident; logs can contain many normal and abnormal events.","log"),
("indicator of compromise","Evidence suggesting that a system or account may have been compromised","Examples can include suspicious hashes, domains, processes, or login activity.","warning"),
("zero trust","A security approach that continuously verifies access instead of automatically trusting based on network location","Zero trust emphasizes explicit verification, least privilege, and assuming breach.","shield"),
("nonrepudiation","Assurance that a party cannot credibly deny performing an action","Digital signatures and trustworthy audit records can help support nonrepudiation.","document"),
]
for term, definition, explanation, icon in terms:
    add("Key Terms & Definitions","definition",
        f"Define the cybersecurity term: {term}.",
        definition, explanation, icon)

# Fill in the blank term recall
for term, definition, explanation, icon in terms:
    add("Key Terms & Definitions","fill_blank",
        f"Fill in the blank: The term for '{definition.lower()}' is □□□□.",
        term, explanation, icon, aliases=[term.lower()])

# ---------------------------------------------------------------------
# SECURITY FUNDAMENTALS
# ---------------------------------------------------------------------

fundamentals = [
("What is the difference between authentication and authorization?",
 "Authentication verifies identity; authorization determines what that authenticated identity is permitted to access or do.",
 "A user normally authenticates first, then authorization rules determine their permissions.","key"),
("Why is multi-factor authentication stronger than a password alone?",
 "MFA requires more than one type of authentication factor, so theft of one factor is less likely to be enough for access.",
 "Common factor categories include something you know, have, and are.","key"),
("What is the purpose of encryption?",
 "Encryption protects readable data by transforming it into ciphertext that requires the appropriate key to decrypt.",
 "Encryption can protect data at rest and data in transit.","lock"),
("What is hashing used for?",
 "Hashing creates a fixed-size one-way digest used for purposes such as integrity checking and secure password-storage systems.",
 "A cryptographic hash is not designed to be decrypted back into the original input.","hash"),
("What is the difference between encryption and hashing?",
 "Encryption is reversible with the appropriate key; cryptographic hashing is designed to be one-way.",
 "They serve different purposes: confidentiality versus integrity/reference representation.","lock"),
("What is salting in password storage?",
 "Salting adds a unique random value to a password before hashing so identical passwords do not produce identical stored hashes.",
 "Salts make precomputed password-hash attacks much less useful.","hash"),
("Why are software patches important?",
 "Patches can fix known vulnerabilities, bugs, and reliability problems before attackers exploit them.",
 "Patch management reduces exposure but should still follow testing and change-control practices.","patch"),
("Why are backups considered a security control?",
 "Backups support recovery from ransomware, accidental deletion, hardware failure, and other destructive events.",
 "Backups should be protected, tested, and ideally separated from the systems they protect.","backup"),
("What does defense in depth mean in practice?",
 "It means combining several independent controls such as MFA, endpoint protection, firewalls, segmentation, logging, backups, and user awareness.",
 "Multiple layers reduce dependence on a single safeguard.","shield"),
("Why is network segmentation useful?",
 "Segmentation limits unnecessary communication between systems and can reduce lateral movement if one area is compromised.",
 "Segmentation supports containment and least privilege at the network level.","network"),
("What is the principle of least privilege?",
 "Users, applications, and services should receive only the minimum access required for their current duties.",
 "This limits damage from compromised credentials or accidental actions.","key"),
("Why is logging important?",
 "Logs provide evidence of activity that helps with detection, troubleshooting, auditing, and investigations.",
 "Useful logging requires sufficient detail, retention, time synchronization, and review.","log"),
("What is the purpose of a firewall?",
 "A firewall permits or blocks network traffic according to security rules.",
 "Firewalls can operate on hosts, network boundaries, cloud environments, and other locations.","firewall"),
("What does an IDS do?",
 "An intrusion detection system monitors activity for suspicious patterns or policy violations and generates alerts.",
 "An IDS primarily detects; blocking is typically associated with an IPS.","radar"),
("What does an IPS do?",
 "An intrusion prevention system detects suspicious activity and can automatically block or prevent it according to configured rules.",
 "IPS controls are usually placed inline with traffic.","radar"),
("What is endpoint detection and response (EDR)?",
 "EDR monitors endpoint activity and provides capabilities for detecting, investigating, and responding to suspicious behavior.",
 "EDR gives defenders richer endpoint visibility than traditional signature-only antivirus.","monitor"),
("What is a VPN?",
 "A virtual private network creates an encrypted tunnel between endpoints, commonly for secure remote access or site-to-site connectivity.",
 "A VPN protects traffic across an untrusted network but does not make all user behavior safe.","network"),
("Why is HTTPS important?",
 "HTTPS uses TLS to protect web traffic in transit and authenticate the server using certificates.",
 "It reduces the risk of passive interception and undetected modification of web traffic.","lock"),
("What does certificate validation help establish?",
 "It helps verify that a certificate is valid for the server name, within its validity period, and chains to a trusted issuer.",
 "Users should not casually bypass certificate warnings.","certificate"),
("What is a digital signature?",
 "A digital signature uses asymmetric cryptography to provide integrity, authenticity, and support for nonrepudiation.",
 "The signer uses a private key; others can verify with the corresponding public key.","certificate"),
]
for q,a,e,icon in fundamentals:
    add("Fundamental Concepts","explanation",q,a,e,icon)

# ---------------------------------------------------------------------
# MALWARE & ATTACK TYPES
# ---------------------------------------------------------------------

attack_terms = [
("phishing","Fraudulent messages designed to trick users into unsafe actions such as revealing credentials or opening malicious content","mail"),
("spear phishing","Highly targeted phishing aimed at a specific person or organization","mail"),
("smishing","Phishing delivered through SMS/text messages","phone"),
("vishing","Voice-call phishing or social engineering","phone"),
("ransomware","Malware that encrypts or otherwise blocks access to systems/data and demands payment","ransom"),
("trojan","Malware disguised as or bundled with something that appears legitimate","bug"),
("worm","Malware capable of self-propagating across systems or networks","bug"),
("virus","Malware that attaches to a host file or program and typically spreads when that host executes","bug"),
("rootkit","Malicious software designed to hide its presence and maintain privileged access","bug"),
("keylogger","Software or hardware that records keystrokes","keyboard"),
("spyware","Software that secretly collects information about a user or system","eye"),
("adware","Software that displays unwanted advertising, sometimes with tracking or potentially unwanted behavior","monitor"),
("botnet","A collection of compromised devices controlled together by an attacker","network"),
("credential stuffing","Using stolen username/password pairs from one breach to attempt logins on other services","key"),
("password spraying","Trying a small number of common passwords across many accounts","key"),
("brute force","Systematically trying many possible credentials or keys until one works","key"),
("tailgating","Following an authorized person into a restricted physical area without proper authentication","door"),
("shoulder surfing","Observing someone entering or viewing sensitive information","eye"),
("pretexting","Creating a fabricated story or identity to persuade a target to disclose information or perform an action","person"),
("baiting","Offering something enticing to persuade a victim to take an unsafe action","hook"),
]
for term,definition,icon in attack_terms:
    add("Threats & Attacks","definition",
        f"What does the security term '{term}' mean?",
        definition,
        f"{term.title()} is a common security concept. Focus on the mechanism that distinguishes it from similar attacks.",
        icon)

# Fill blanks for attacks
for term,definition,icon in attack_terms:
    add("Threats & Attacks","fill_blank",
        f"Fill in the blank: {definition}. This attack or malware type is called □□□□.",
        term,
        f"The defining clue is the method described in the sentence.",
        icon, aliases=[term.lower()])

# ---------------------------------------------------------------------
# NETWORK & PROTOCOL FUNDAMENTALS
# ---------------------------------------------------------------------

network_items = [
("What does DNS do?","DNS resolves human-readable names to IP addresses and can also provide other resource records.","DNS acts like a distributed naming directory for networks.","dns"),
("What does DHCP do?","DHCP automatically provides hosts with network configuration such as an IP address, subnet mask, default gateway, and DNS servers.","It reduces the need for manual IP configuration.","network"),
("What is the purpose of a default gateway?","It is the router a host sends traffic to when the destination is outside the local network.","Without a working gateway, local communication may work while remote destinations fail.","router"),
("What is the difference between TCP and UDP?","TCP is connection-oriented and provides reliable ordered delivery; UDP is connectionless and lower overhead without built-in delivery guarantees.","Different applications choose the protocol that best matches reliability and latency needs.","network"),
("What is a network port?","A port number identifies a logical application or service endpoint on a host.","Ports let one IP address support many simultaneous network services.","network"),
("What is the purpose of DNS over HTTPS or DNS over TLS?","They encrypt DNS queries between the client and the configured resolver.","Encryption can reduce passive observation or modification of DNS traffic on the path.","dns"),
("Why can an open network port increase attack surface?","A listening service may contain vulnerabilities or expose functionality to attackers.","Only necessary services should be exposed, and they should be securely configured and patched.","firewall"),
("What is network segmentation?","Dividing a network into controlled zones or segments with restricted communication between them.","Segmentation can limit lateral movement and reduce the blast radius of a compromise.","network"),
("What is a VLAN?","A virtual LAN logically separates Layer 2 network segments on switching infrastructure.","VLANs are commonly used as part of network segmentation designs.","network"),
("What is NAT?","Network Address Translation changes address information as traffic passes through a network device, commonly translating private addresses to public addresses.","NAT is not a replacement for a firewall or security policy.","router"),
]
for q,a,e,icon in network_items:
    add("Networking & Security","explanation",q,a,e,icon)

# ---------------------------------------------------------------------
# SCENARIOS
# ---------------------------------------------------------------------

scenarios = [
("A user reports an unexpected MFA approval prompt. What should they do?",
 "Deny the prompt, do not approve it, report the event, and review or protect the account according to organizational policy.",
 "Unexpected MFA prompts can be a sign that someone already has the password or is attempting an MFA-fatigue attack.","key"),
("A user says they entered their password on a page reached from a suspicious email. What should happen next?",
 "Treat it as a potential credential compromise: reset the password through the approved process, revoke active sessions where possible, verify MFA, review account activity, and notify security.",
 "Speed matters because compromised credentials may already be in use.","mail"),
("You find an unknown USB drive in the parking lot. What should you do?",
 "Do not connect it to a company computer. Turn it over to the appropriate IT or security team according to policy.",
 "Unknown removable media can contain malware or malicious hardware.","usb"),
("A caller claims to be a senior executive and urgently asks you to bypass identity verification for a password reset. What should you do?",
 "Follow the normal identity-verification and password-reset process regardless of title or urgency.",
 "Social engineering frequently relies on authority and urgency to pressure people into bypassing controls.","phone"),
("A workstation suddenly shows a ransomware demand. What is the first security priority?",
 "Contain the potential incident according to policy, such as isolating the affected device from the network, and notify the incident-response or security team.",
 "Containment can help reduce further spread while preserving evidence for investigation.","ransom"),
("A browser displays a certificate warning on an internal business site. What should the user do?",
 "Stop rather than clicking through, verify the site address, capture the warning details, and report the issue to IT/security.",
 "Certificate warnings can result from misconfiguration or interception and should be investigated.","certificate"),
("You discover that a shared folder grants full control to everyone in the company. What security principle is most relevant?",
 "Least privilege.",
 "Permissions should be limited to the users and actions actually required.","key"),
("A terminated employee still has an active cloud account. What should happen?",
 "Disable or suspend access promptly, revoke active sessions/tokens, remove group/application access, and follow the offboarding process.",
 "Timely deprovisioning reduces the risk of unauthorized post-employment access.","cloud"),
("A user installs an unknown browser extension that requests permission to read and change data on all websites. What should you do?",
 "Verify whether the extension is approved and needed. If it is unauthorized or suspicious, remove or disable it according to policy and check for related account or browser changes.",
 "Broad browser permissions can expose credentials and sensitive browsing data.","browser"),
("A user asks you to turn off antivirus because it blocks a downloaded file. What should you do?",
 "Do not disable protection simply to make the file run. Verify the file source and use the approved security exception or escalation process.",
 "Security controls should not be bypassed for convenience.","shield"),
("An employee emails confidential data to a personal account so they can work at home. Why is this a concern?",
 "It may move sensitive data outside approved organizational controls and violate data-handling policy.",
 "Use approved remote-access and file-sharing methods instead.","mail"),
("You notice many failed logins against one account from unfamiliar locations. What should you do?",
 "Treat the activity as suspicious, verify with the account owner, review available sign-in information, protect the account, and escalate according to policy.",
 "Repeated failures may indicate password guessing, credential stuffing, or another attack.","log"),
("A coworker asks to use your account because their account is locked. What should you do?",
 "Do not share your account or credentials. Help them restore their own access through the approved process.",
 "Shared accounts reduce accountability and can violate access-control policy.","key"),
("A laptop containing company data is lost. What actions are important?",
 "Report it immediately, provide last-known details, use approved remote-lock or wipe capabilities where available, and protect associated accounts.",
 "Lost devices are both physical-security and data-security incidents.","laptop"),
("A user says their email is automatically forwarding to an address they do not recognize. What might this indicate?",
 "Possible account compromise. Remove unauthorized rules through the approved process, protect the account, revoke sessions, review sign-in activity, and report the incident.",
 "Attackers sometimes create forwarding rules to silently collect messages.","mail"),
]
for q,a,e,icon in scenarios:
    add("Security Scenarios","scenario",q,a,e,icon)

# Generate scenario variations for a large bank.
scenario_subjects = [
    ("employee laptop","shows an antivirus alert for an unknown executable","endpoint"),
    ("email account","has a successful login from an unfamiliar country","key"),
    ("file server","has a new administrator account nobody recognizes","server"),
    ("cloud storage account","contains a public link to a confidential folder","cloud"),
    ("Wi-Fi network","shows an unfamiliar access point using the company name","wifi"),
    ("workstation","starts making connections to many suspicious domains","network"),
    ("browser","has an unfamiliar extension installed","browser"),
    ("administrator account","receives repeated MFA requests","key"),
]
scenario_actions = {
"endpoint":"Preserve details from the alert, avoid running the file, isolate the system if policy requires, and escalate to the security team.",
"key":"Protect the account, verify activity with the user, revoke suspicious sessions, change credentials where required, and report the event.",
"server":"Verify whether the change was authorized, preserve logs/evidence, limit exposure according to policy, and escalate promptly.",
"cloud":"Remove unsafe public exposure through the approved process, verify access requirements, review logs, and notify the data owner/security team.",
"wifi":"Do not connect automatically. Verify approved wireless infrastructure and notify networking/security because the access point may be an evil twin.",
"network":"Identify the involved process or device, contain it according to policy, preserve evidence, and escalate to security.",
"browser":"Verify whether the extension is approved, review its permissions, remove or disable it if unauthorized, and check for suspicious browser/account changes."
}
for asset, condition, tag in scenario_subjects:
    for urgency in ["during normal support hours","while the user is working remotely","after a recent software update"]:
        add("Security Scenarios","scenario",
            f"You discover that an {asset} {condition} {urgency}. As an entry-level technician, what should you do?",
            scenario_actions[tag],
            "A strong answer prioritizes safety, evidence preservation, approved procedures, clear documentation, and appropriate escalation.",
            tag if tag in {"key","server","cloud","wifi","network","browser"} else "shield")

# ---------------------------------------------------------------------
# MATCHING QUESTIONS
# ---------------------------------------------------------------------

matching_sets = [
("Match each security objective to its description.",
 [("Confidentiality","Prevents unauthorized disclosure"),
  ("Integrity","Protects accuracy and prevents unauthorized modification"),
  ("Availability","Keeps systems and information accessible when needed")],
 "CIA triad objectives are distinct but complementary.","shield"),
("Match each authentication factor category to an example.",
 [("Something you know","Password or PIN"),
  ("Something you have","Hardware token or phone"),
  ("Something you are","Fingerprint or face biometric")],
 "Strong MFA combines factors from different categories.","key"),
("Match each malware type to its characteristic.",
 [("Ransomware","Encrypts or blocks data and demands payment"),
  ("Worm","Can self-propagate across systems"),
  ("Trojan","Disguises itself as legitimate software")],
 "Focus on the primary behavior that distinguishes each malware type.","bug"),
("Match each social-engineering term to its delivery method.",
 [("Phishing","Email or general electronic message"),
  ("Smishing","SMS or text message"),
  ("Vishing","Voice call")],
 "The delivery channel distinguishes these common phishing variants.","mail"),
("Match each security activity to its role.",
 [("Preventive control","Attempts to stop an unwanted event"),
  ("Detective control","Identifies or alerts on unwanted activity"),
  ("Corrective control","Helps restore or repair after an event")],
 "Controls are often classified by when they act relative to an incident.","shield"),
("Match each network component to its primary role.",
 [("Router","Forwards traffic between IP networks"),
  ("Switch","Connects devices within a local Ethernet network"),
  ("Firewall","Allows or blocks traffic according to security rules")],
 "Each device can have additional features, but these are the core roles.","network"),
("Match each term to the question it answers.",
 [("Authentication","Who are you?"),
  ("Authorization","What are you allowed to do?"),
  ("Accounting","What activity occurred?")],
 "This grouping is sometimes remembered as AAA.","key"),
("Match each security document type to its purpose.",
 [("Policy","High-level mandatory expectations"),
  ("Procedure","Step-by-step instructions"),
  ("Guideline","Recommended flexible guidance")],
 "Organizations use different document types to express governance at different levels.","document"),
("Match each security property to a technology commonly associated with it.",
 [("Confidentiality","Encryption"),
  ("Integrity","Cryptographic hashing"),
  ("Availability","Redundancy and backups")],
 "A technology can support multiple goals, but each pairing reflects a common primary use.","shield"),
("Match each attack to its typical method.",
 [("Credential stuffing","Reuse previously stolen username/password pairs"),
  ("Password spraying","Try a small set of common passwords across many accounts"),
  ("Brute force","Try many possible passwords against a target")],
 "The difference is mainly how candidate credentials are selected and distributed across accounts.","key"),
]
for prompt,pairs,exp,icon in matching_sets:
    answer = "; ".join(f"{a} → {b}" for a,b in pairs)
    add("Matching","matching",prompt,answer,exp,icon,match_items=pairs)

# Generate more matching sets by grouping 3 terms at a time.
extra_pairs = [
("VPN","Encrypted tunnel for secure network access"),
("EDR","Endpoint monitoring, investigation, and response"),
("IDS","Detects suspicious activity and raises alerts"),
("IPS","Detects and can automatically block suspicious activity"),
("DNS","Resolves names to IP addresses"),
("DHCP","Automatically assigns network configuration"),
("Hash","One-way digest of input data"),
("Encryption","Reversible protection using a key"),
("Digital signature","Supports authenticity and integrity"),
("Backup","Recovery copy of data"),
("Patch","Software update that can fix vulnerabilities"),
("Vulnerability","Weakness that could be exploited"),
]
for i in range(0, len(extra_pairs)-2, 3):
    group = extra_pairs[i:i+3]
    if len(group)==3:
        answer = "; ".join(f"{a} → {b}" for a,b in group)
        add("Matching","matching",
            "Match each cybersecurity term to the best description.",
            answer,
            "Compare the primary function of each term rather than looking for keyword overlap.",
            "network", match_items=group)

# ---------------------------------------------------------------------
# FILL-IN-THE-BLANK FUNDAMENTALS
# ---------------------------------------------------------------------

fills = [
("The security principle of giving a user only the permissions needed for their job is called □□□□.","least privilege","This principle limits unnecessary access.","key"),
("A fraudulent message designed to steal credentials is commonly called □□□□.","phishing","The clue is deceptive messaging intended to trigger an unsafe action.","mail"),
("A one-way cryptographic digest of data is called a □□□□.","hash","It is commonly used for integrity checks.","hash"),
("A security device or software control that filters network traffic according to rules is a □□□□.","firewall","It controls traffic based on policy.","firewall"),
("The three goals confidentiality, integrity, and availability are called the □□□□.","CIA triad","These are foundational information-security objectives.","shield"),
("Software that encrypts files and demands payment is called □□□□.","ransomware","The defining feature is denial of access paired with a demand for payment.","ransom"),
("A weakness that could be exploited by a threat is called a □□□□.","vulnerability","It is the weakness side of threat–vulnerability–risk analysis.","bug"),
("A safeguard implemented to reduce risk is called a security □□□□.","control","Safeguards can be technical, administrative, or physical.","shield"),
("A network tunnel used to securely connect across an untrusted network is commonly called a □□□□.","VPN","It is frequently used for remote access.","network"),
("The process of verifying who a user is is called □□□□.","authentication","This occurs before permissions are evaluated.","key"),
("The process of deciding what an authenticated user may do is called □□□□.","authorization","It determines permissions after identity is established.","key"),
("A copy of data maintained so it can be restored after loss is a □□□□.","backup","This supports recovery and availability.","backup"),
("Malware that can spread by itself across systems is called a □□□□.","worm","Self-propagation is the key clue.","bug"),
("Phishing performed through text messages is called □□□□.","smishing","The term combines SMS and phishing.","phone"),
("Phishing performed over voice calls is called □□□□.","vishing","The term combines voice and phishing.","phone"),
]
for q,a,e,icon in fills:
    add("Fill in the Blank","fill_blank",q,a,e,icon,aliases=[a.lower()])

# ---------------------------------------------------------------------
# OBJECTIVE SINGLE-SELECT QUESTIONS
# ---------------------------------------------------------------------

mcqs = [
("Which option best represents a preventive security control?",
 ["Firewall rule blocking unauthorized inbound traffic","Security log review after an incident","Forensic disk image","Post-incident lessons-learned meeting"],
 "Firewall rule blocking unauthorized inbound traffic",
 "Preventive controls attempt to stop unwanted activity before or as it occurs.","firewall"),
("Which option is an example of 'something you have'?",
 ["Password","Security token","Fingerprint","Security question"],
 "Security token",
 "Possession factors are physical or digital items the user possesses.","key"),
("Which protocol is primarily used to translate host names into IP addresses?",
 ["DNS","DHCP","SSH","NTP"],
 "DNS",
 "DNS provides name-resolution services.","dns"),
("Which principle most directly limits the damage possible from a compromised user account?",
 ["Least privilege","Open access","Password reuse","Shared accounts"],
 "Least privilege",
 "Restricting permissions reduces what a compromised account can reach or modify.","key"),
("Which action is safest after finding an unknown USB device?",
 ["Plug it into a spare company computer","Open it only while disconnected from Wi-Fi","Turn it over to IT/security without connecting it","Format it on your workstation"],
 "Turn it over to IT/security without connecting it",
 "Unknown removable media should be treated as potentially malicious.","usb"),
("Which item most directly supports recovery from ransomware?",
 ["Tested offline or isolated backups","A longer monitor cable","A public Wi-Fi hotspot","Disabling audit logs"],
 "Tested offline or isolated backups",
 "Protected and tested backups can allow restoration without relying on the attacker.","backup"),
("Which technology is designed to create a one-way digest?",
 ["Cryptographic hash function","Symmetric encryption","VPN tunnel","Firewall"],
 "Cryptographic hash function",
 "Hash functions are designed to produce one-way digests.","hash"),
("Which option best describes an IDS?",
 ["A system that primarily detects suspicious activity and alerts","A system used only to create backups","A password manager","A disk-encryption feature"],
 "A system that primarily detects suspicious activity and alerts",
 "IDS stands for intrusion detection system.","radar"),
("Which term describes a highly targeted phishing attack?",
 ["Spear phishing","Smishing","Brute force","Tailgating"],
 "Spear phishing",
 "Spear phishing is customized for a particular target or organization.","mail"),
("Which protocol is connection-oriented and provides reliable ordered delivery?",
 ["TCP","UDP","ARP","ICMP"],
 "TCP",
 "TCP establishes a connection and tracks reliable ordered delivery.","network"),
]
for q, choices, correct, exp, icon in mcqs:
    add("Multiple Choice","multiple_choice",q,correct,exp,icon,choices=choices,correct=correct)

# Generate many additional objective questions from terms.
for term, definition, explanation, icon in terms[:20]:
    distractors = [x[0] for x in terms if x[0] != term]
    random.seed(term)
    wrong = random.sample(distractors, 3)
    choices = wrong + [term]
    random.shuffle(choices)
    add("Key Terms & Definitions","multiple_choice",
        f"Which term best matches this definition: {definition}?",
        term, explanation, icon, choices=choices, correct=term)

# ---------------------------------------------------------------------
# VECTOR ART
# ---------------------------------------------------------------------

class VectorArt(tk.Canvas):
    def __init__(self, master, width=280, height=205, **kwargs):
        super().__init__(master, width=width, height=height,
                         bg="#071a35", highlightthickness=0, **kwargs)
        self.w = width
        self.h = height

    def clear(self):
        self.delete("all")
        self.create_rectangle(0,0,self.w,self.h,fill="#071a35",outline="")
        # subtle vector grid / node pattern
        for x in range(20,self.w,52):
            for y in range(25,self.h,52):
                self.create_oval(x-2,y-2,x+2,y+2,fill="#184a7f",outline="")
        for x in range(20,self.w-52,52):
            self.create_line(x,25,x+52,77,fill="#0f365e",width=1)
            self.create_line(x,129,x+52,77,fill="#0f365e",width=1)

    def shield(self):
        self.create_polygon(140,28,205,53,195,120,140,172,85,120,75,53,
                            fill="#0f4380",outline="#4fc3ff",width=4)
        self.create_line(140,49,140,145,fill="#65d2ff",width=4)
        self.create_line(104,91,132,118,177,72,fill="#a4f0ff",width=7)

    def lock(self):
        self.create_arc(93,32,187,119,start=0,extent=180,style="arc",
                        outline="#67d5ff",width=12)
        self.create_rectangle(77,86,203,166,fill="#124d87",outline="#68d7ff",width=4)
        self.create_oval(130,107,150,127,fill="#d7f7ff",outline="")
        self.create_rectangle(137,124,143,147,fill="#d7f7ff",outline="")

    def key(self):
        self.create_oval(61,65,126,130,fill="#0d447e",outline="#62d5ff",width=5)
        self.create_oval(83,87,104,108,fill="#071a35",outline="#62d5ff",width=3)
        self.create_line(119,112,213,154,fill="#69dbff",width=14)
        self.create_line(175,137,188,116,fill="#69dbff",width=10)
        self.create_line(195,147,208,126,fill="#69dbff",width=10)

    def mail(self):
        self.create_rectangle(48,55,232,157,fill="#103f75",outline="#58c9ff",width=4)
        self.create_line(49,58,140,117,232,58,fill="#8ce2ff",width=4)
        self.create_line(49,156,111,105,fill="#3a9ee0",width=3)
        self.create_line(232,156,169,105,fill="#3a9ee0",width=3)
        self.create_arc(185,112,243,170,start=30,extent=250,style="arc",outline="#ffbd59",width=5)

    def network(self):
        pts=[(58,57),(140,38),(219,66),(83,146),(174,145)]
        for a,b in [(0,1),(1,2),(0,3),(1,3),(1,4),(2,4),(3,4)]:
            self.create_line(*pts[a],*pts[b],fill="#3198d7",width=3)
        for x,y in pts:
            self.create_oval(x-13,y-13,x+13,y+13,fill="#0d569c",outline="#71dcff",width=3)

    def bug(self):
        self.create_oval(102,55,178,148,fill="#0f4b83",outline="#63d4ff",width=4)
        self.create_oval(115,36,165,76,fill="#174f84",outline="#63d4ff",width=4)
        for y in [78,101,124]:
            self.create_line(103,y,69,y-16,fill="#63d4ff",width=4)
            self.create_line(177,y,211,y-16,fill="#63d4ff",width=4)
        self.create_line(126,39,111,22,fill="#63d4ff",width=3)
        self.create_line(154,39,169,22,fill="#63d4ff",width=3)

    def server(self):
        for y in [43,88,133]:
            self.create_rectangle(62,y,218,y+34,fill="#103e70",outline="#61cff9",width=3)
            self.create_oval(78,y+12,88,y+22,fill="#78ebae",outline="")
            self.create_line(109,y+17,194,y+17,fill="#338ec7",width=3)

    def warning(self):
        self.create_polygon(140,30,225,166,55,166,fill="#684b0e",outline="#ffd166",width=5)
        self.create_line(140,73,140,125,fill="#fff2b2",width=10)
        self.create_oval(134,139,146,151,fill="#fff2b2",outline="")

    def log(self):
        self.create_rectangle(62,34,218,170,fill="#103c6d",outline="#62cdf5",width=4)
        for y in [62,88,114,140]:
            self.create_oval(79,y-4,87,y+4,fill="#66e0ff",outline="")
            self.create_line(99,y,193,y,fill="#5aa7d8",width=4)

    def document(self):
        self.create_polygon(83,28,179,28,213,62,213,171,83,171,
                            fill="#103f72",outline="#62d0ff",width=4)
        self.create_polygon(179,28,179,62,213,62,fill="#1c619a",outline="#62d0ff",width=3)
        for y in [86,110,134,158]:
            self.create_line(105,y,188,y,fill="#75c9ed",width=4)

    def hash(self):
        self.create_text(140,101,text="#",fill="#71dcff",font=("Helvetica",88,"bold"))

    def backup(self):
        self.create_oval(62,112,218,164,fill="#103f71",outline="#5ecfff",width=4)
        self.create_rectangle(62,76,218,138,fill="#103f71",outline="#5ecfff",width=4)
        self.create_arc(75,49,205,124,start=20,extent=285,style="arc",outline="#75e8ae",width=7)
        self.create_polygon(78,67,97,49,99,77,fill="#75e8ae",outline="")

    def firewall(self):
        for row in range(4):
            y=43+row*30
            offset=0 if row%2==0 else 20
            for col in range(4):
                x=58+offset+col*42
                self.create_rectangle(x,y,x+38,y+24,fill="#174c7e",outline="#62cffa",width=2)
        self.create_line(140,30,140,179,fill="#ff8364",width=5)

    def radar(self):
        self.create_oval(70,34,210,174,outline="#55caff",width=3)
        self.create_oval(96,60,184,148,outline="#338ec7",width=2)
        self.create_oval(121,85,159,123,outline="#338ec7",width=2)
        self.create_line(140,104,197,61,fill="#74e9b1",width=4)
        self.create_oval(187,58,199,70,fill="#ffca62",outline="")

    def monitor(self):
        self.create_rectangle(54,40,226,148,fill="#0c3159",outline="#5bceff",width=4)
        self.create_line(140,148,140,172,fill="#5bceff",width=5)
        self.create_line(105,173,175,173,fill="#5bceff",width=5)
        self.create_line(76,114,104,94,124,108,149,67,176,101,207,73,fill="#74e8ae",width=4)

    def certificate(self):
        self.document()
        self.create_oval(151,118,202,169,fill="#8b5c13",outline="#ffd166",width=4)
        self.create_text(176,143,text="✓",fill="#fff3bd",font=("Helvetica",26,"bold"))

    def phone(self):
        self.create_rectangle(93,25,187,179,fill="#0e3a68",outline="#5dd0fb",width=4)
        self.create_rectangle(105,45,175,146,fill="#071a35",outline="#2e7fb8",width=2)
        self.create_oval(133,157,147,171,fill="#70dcff",outline="")

    def keyboard(self):
        self.create_polygon(54,85,226,85,244,156,36,156,fill="#103e70",outline="#60cefa",width=4)
        for r in range(3):
            for c in range(8):
                x=55+c*20+(r%2)*4
                y=97+r*16
                self.create_rectangle(x,y,x+14,y+10,fill="#1c6097",outline="")

    def eye(self):
        self.create_arc(48,54,232,156,start=200,extent=140,style="arc",outline="#5dd4ff",width=6)
        self.create_arc(48,54,232,156,start=20,extent=140,style="arc",outline="#5dd4ff",width=6)
        self.create_oval(116,78,164,126,fill="#1a71a8",outline="#75e4ff",width=4)
        self.create_oval(132,94,148,110,fill="#071a35",outline="")

    def door(self):
        self.create_rectangle(84,28,196,177,fill="#123f6d",outline="#60cff8",width=4)
        self.create_rectangle(105,46,182,177,fill="#0c3155",outline="#3b8abd",width=3)
        self.create_oval(163,109,173,119,fill="#ffce63",outline="")

    def person(self):
        self.create_oval(111,34,169,92,fill="#1c5c91",outline="#68d7ff",width=4)
        self.create_arc(72,85,208,194,start=0,extent=180,style="pieslice",fill="#124774",outline="#68d7ff",width=4)

    def hook(self):
        self.create_arc(87,35,193,151,start=40,extent=270,style="arc",outline="#ffcb61",width=8)
        self.create_line(192,120,221,141,fill="#ffcb61",width=8)

    def usb(self):
        self.create_rectangle(80,76,183,136,fill="#124a7c",outline="#62d4ff",width=4)
        self.create_rectangle(183,87,224,125,fill="#8ccce8",outline="#d9f7ff",width=3)
        self.create_line(198,94,198,118,fill="#315a70",width=3)
        self.create_line(210,94,210,118,fill="#315a70",width=3)
        self.create_rectangle(57,92,80,120,fill="#1f6599",outline="#62d4ff",width=3)

    def ransom(self):
        self.lock()
        self.create_text(140,181,text="$",fill="#ffd166",font=("Helvetica",24,"bold"))

    def cloud(self):
        self.create_oval(74,82,143,146,fill="#154d7c",outline="#65d5ff",width=4)
        self.create_oval(112,52,181,139,fill="#154d7c",outline="#65d5ff",width=4)
        self.create_oval(153,78,218,146,fill="#154d7c",outline="#65d5ff",width=4)
        self.create_rectangle(92,112,199,148,fill="#154d7c",outline="")
        self.create_line(116,119,164,119,fill="#82e9b5",width=5)
        self.create_line(140,96,140,143,fill="#82e9b5",width=5)

    def wifi(self):
        for r,w in [(42,5),(68,5),(94,5)]:
            self.create_arc(140-r,40,140+r,40+2*r,start=40,extent=100,style="arc",outline="#63d5ff",width=w)
        self.create_oval(133,146,147,160,fill="#7ae7b5",outline="")

    def browser(self):
        self.create_rectangle(45,38,235,166,fill="#0d345e",outline="#61cff9",width=4)
        self.create_rectangle(45,38,235,68,fill="#174b7c",outline="#61cff9",width=3)
        for x in [61,78,95]:
            self.create_oval(x,49,x+8,57,fill="#7edfff",outline="")
        self.create_polygon(120,87,158,87,176,120,157,151,120,151,101,120,
                            fill="#1c669a",outline="#74e5ff",width=3)

    def router(self):
        self.create_rectangle(62,104,218,153,fill="#123f6b",outline="#61d0fb",width=4)
        self.create_line(94,105,80,51,fill="#61d0fb",width=4)
        self.create_line(186,105,200,51,fill="#61d0fb",width=4)
        for x in [88,111,134]:
            self.create_oval(x,123,x+9,132,fill="#77ecad",outline="")

    def dns(self):
        self.network()
        self.create_text(140,102,text="DNS",fill="#ffffff",font=("Helvetica",24,"bold"))

    def laptop(self):
        self.create_rectangle(67,35,213,137,fill="#0b3159",outline="#62d1fb",width=4)
        self.create_polygon(47,146,233,146,251,169,29,169,fill="#154f7d",outline="#62d1fb",width=3)

    def patch(self):
        self.create_rectangle(75,47,205,159,fill="#113e6e",outline="#65d4ff",width=4)
        self.create_line(105,102,132,129,179,77,fill="#7aebb4",width=9)

    def endpoint(self):
        self.monitor()
        self.create_polygon(202,105,235,118,231,153,202,180,173,153,169,118,
                            fill="#0e487c",outline="#72ddff",width=3)

    def draw(self, icon):
        self.clear()
        fn = getattr(self, icon, None)
        if fn is None:
            fn = self.shield
        fn()
        self.create_text(self.w//2,191,text=icon.replace("_"," ").upper(),
                         fill="#548bb8",font=("Helvetica",9,"bold"))

# ---------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------

TYPE_LABELS = {
    "definition":"Definition",
    "fill_blank":"Fill in the Blank",
    "explanation":"Explain",
    "scenario":"Scenario",
    "matching":"Matching",
    "multiple_choice":"Multiple Choice",
}

class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(1050,720)
        self.configure(bg="#05142c")

        self.current = None
        self.session_seen = set()
        self.objective_attempted = 0
        self.objective_correct = 0
        self.choice_var = tk.StringVar(value="")
        self.match_vars = []

        self._styles()
        self._build()

    def _styles(self):
        st = ttk.Style(self)
        try:
            st.theme_use("clam")
        except tk.TclError:
            pass

        bg="#05142c"; panel="#0a2247"; panel2="#0d2b58"; ink="#edf8ff"
        st.configure("Root.TFrame",background=bg)
        st.configure("Panel.TFrame",background=panel)
        st.configure("Card.TFrame",background=panel2)
        st.configure("Root.TLabel",background=bg,foreground=ink,font=("Helvetica",11))
        st.configure("Panel.TLabel",background=panel,foreground=ink,font=("Helvetica",11))
        st.configure("Title.TLabel",background=panel,foreground="white",font=("Helvetica",25,"bold"))
        st.configure("Subtitle.TLabel",background=panel,foreground="#a9d1f0",font=("Helvetica",11))
        st.configure("QuestionType.TLabel",background=panel2,foreground="#6fd3ff",font=("Helvetica",11,"bold"))
        st.configure("Question.TLabel",background=panel2,foreground="white",font=("Helvetica",17,"bold"))
        st.configure("Helper.TLabel",background=panel2,foreground="#b5d6ec",font=("Helvetica",10,"italic"))
        st.configure("Answer.TLabel",background="#10385d",foreground="#effcff",font=("Helvetica",12))
        st.configure("Score.TLabel",background=bg,foreground="#7ee5b0",font=("Helvetica",11,"bold"))

        st.configure("Q.TLabelframe",background=panel2,foreground="white")
        st.configure("Q.TLabelframe.Label",background=panel2,foreground="#70d8ff",font=("Helvetica",11,"bold"))
        st.configure("A.TLabelframe",background="#10385d",foreground="white")
        st.configure("A.TLabelframe.Label",background="#10385d",foreground="#83efb6",font=("Helvetica",11,"bold"))

        st.configure("Accent.TButton",background="#178fff",foreground="white",
                     font=("Helvetica",11,"bold"),padding=(16,9),borderwidth=0)
        st.map("Accent.TButton",background=[("active","#37a6ff")])
        st.configure("Secondary.TButton",background="#173f75",foreground="white",
                     font=("Helvetica",10,"bold"),padding=(13,8),borderwidth=0)
        st.map("Secondary.TButton",
               background=[("active","#245792"),("disabled","#26394d")],
               foreground=[("disabled","#8091a5")])
        st.configure("Choice.TRadiobutton",background=panel2,foreground="white",
                     font=("Helvetica",11),padding=3)
        st.map("Choice.TRadiobutton",background=[("active",panel2)])
        st.configure("TCombobox",fieldbackground="#f3f8fc",foreground="#10243c",padding=6)

    def _build(self):
        root = ttk.Frame(self,style="Root.TFrame",padding=18)
        root.pack(fill="both",expand=True)

        header = ttk.Frame(root,style="Panel.TFrame",padding=16)
        header.pack(fill="x",pady=(0,12))
        ttk.Label(header,text="Cybersecurity Fundamentals Quiz",style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text=f"{len(QUESTIONS)} embedded questions • definitions • concepts • scenarios • matching • fill-in-the-blank",
            style="Subtitle.TLabel"
        ).pack(anchor="w",pady=(4,0))

        controls = ttk.Frame(root,style="Root.TFrame")
        controls.pack(fill="x",pady=(0,10))

        ttk.Label(controls,text="Category:",style="Root.TLabel").pack(side="left")
        self.category_var=tk.StringVar(value="All Categories")
        categories=["All Categories"]+sorted({q["category"] for q in QUESTIONS})
        ttk.Combobox(controls,textvariable=self.category_var,values=categories,
                     state="readonly",width=25).pack(side="left",padx=(8,12))

        ttk.Label(controls,text="Question type:",style="Root.TLabel").pack(side="left")
        self.type_var=tk.StringVar(value="All Types")
        types=["All Types"]+[TYPE_LABELS[t] for t in sorted(TYPE_LABELS)]
        ttk.Combobox(controls,textvariable=self.type_var,values=types,
                     state="readonly",width=20).pack(side="left",padx=(8,12))

        ttk.Button(controls,text="Generate Question",command=self.generate,
                   style="Accent.TButton").pack(side="left")
        ttk.Button(controls,text="Reset Session",command=self.reset_session,
                   style="Secondary.TButton").pack(side="left",padx=(10,0))

        self.score_label=ttk.Label(controls,text="Session score: 0 / 0",style="Score.TLabel")
        self.score_label.pack(side="right")

        content=ttk.Frame(root,style="Root.TFrame")
        content.pack(fill="both",expand=True)
        content.columnconfigure(0,weight=1)
        content.columnconfigure(1,weight=0)
        content.rowconfigure(0,weight=1)

        left=ttk.Frame(content,style="Root.TFrame")
        left.grid(row=0,column=0,sticky="nsew",padx=(0,12))

        qbox=ttk.LabelFrame(left,text=" Question ",style="Q.TLabelframe",padding=16)
        qbox.pack(fill="x",pady=(0,10))

        self.meta_label=ttk.Label(qbox,text="",style="QuestionType.TLabel")
        self.meta_label.pack(anchor="w")
        self.question_label=ttk.Label(
            qbox,text="Click Generate Question to begin.",
            style="Question.TLabel",wraplength=790,justify="left"
        )
        self.question_label.pack(fill="x",anchor="w",pady=(7,5))
        self.helper_label=ttk.Label(
            qbox,text="",
            style="Helper.TLabel",wraplength=790,justify="left"
        )
        self.helper_label.pack(fill="x",anchor="w")

        self.response_box=ttk.LabelFrame(left,text=" Your Answer ",style="Q.TLabelframe",padding=13)
        self.response_box.pack(fill="both",expand=True,pady=(0,10))

        self.dynamic = ttk.Frame(self.response_box,style="Card.TFrame")
        self.dynamic.pack(fill="both",expand=True)

        actions=ttk.Frame(left,style="Root.TFrame")
        actions.pack(fill="x")
        self.reveal_btn=ttk.Button(
            actions,text="Reveal Sample Answer",command=self.reveal,
            state="disabled",style="Secondary.TButton"
        )
        self.reveal_btn.pack(side="left")
        ttk.Button(actions,text="Clear Answer",command=self.clear_response,
                   style="Secondary.TButton").pack(side="left",padx=(9,0))

        self.answer_frame=ttk.LabelFrame(
            left,text=" Sample Answer & Explanation ",
            style="A.TLabelframe",padding=14
        )
        self.answer_label=ttk.Label(
            self.answer_frame,text="",style="Answer.TLabel",
            wraplength=790,justify="left"
        )
        self.answer_label.pack(fill="x")

        right=ttk.Frame(content,style="Panel.TFrame",padding=10)
        right.grid(row=0,column=1,sticky="n",padx=(0,0))
        ttk.Label(right,text="Question Visual",style="Panel.TLabel").pack(anchor="center",pady=(0,6))
        self.art=VectorArt(right)
        self.art.pack()
        self.art.draw("shield")
        self.pool_label=ttk.Label(right,text="",style="Panel.TLabel",wraplength=270,justify="center")
        self.pool_label.pack(pady=(10,0))

        self.status=ttk.Label(
            root,
            text="Answer first; the sample-answer button unlocks after you make an attempt.",
            style="Root.TLabel"
        )
        self.status.pack(anchor="w",pady=(10,0))

        self._show_text_entry()

    def _selected_type(self):
        selected=self.type_var.get()
        if selected=="All Types":
            return None
        for key,label in TYPE_LABELS.items():
            if label==selected:
                return key
        return None

    def _pool(self):
        cat=self.category_var.get()
        qtype=self._selected_type()
        pool=QUESTIONS
        if cat!="All Categories":
            pool=[q for q in pool if q["category"]==cat]
        if qtype:
            pool=[q for q in pool if q["type"]==qtype]
        return pool

    def generate(self):
        pool=self._pool()
        if not pool:
            messagebox.showinfo("No Questions","No questions match those filters.")
            return

        unseen=[q for q in pool if id(q) not in self.session_seen]
        if not unseen:
            self.session_seen.clear()
            unseen=pool

        if self.current and len(unseen)>1:
            choices=[q for q in unseen if q is not self.current]
            self.current=random.choice(choices or unseen)
        else:
            self.current=random.choice(unseen)

        self.session_seen.add(id(self.current))
        self.meta_label.config(
            text=f'{self.current["category"]}  •  {TYPE_LABELS[self.current["type"]]}'
        )
        self.question_label.config(text=self.current["question"])
        self.helper_label.config(text=self._helper_text(self.current["type"]))
        self.art.draw(self.current["icon"])
        self.pool_label.config(
            text=f"{len(pool)} questions match the current filters.\n"
                 f"{len(self.session_seen)} question(s) seen this session."
        )
        self.clear_response()
        self._make_response_ui()
        self.status.config(text="Give your best answer before revealing the sample.")
        self.answer_frame.pack_forget()

    def _helper_text(self,qtype):
        return {
            "definition":"Explain the meaning in your own words.",
            "explanation":"Explain the concept clearly enough for a new IT employee.",
            "scenario":"Describe what you would do and why.",
            "fill_blank":"Type the missing cybersecurity term.",
            "matching":"Enter the matching letter/description for each term.",
            "multiple_choice":"Select the best answer."
        }.get(qtype,"")

    def _clear_dynamic(self):
        for w in self.dynamic.winfo_children():
            w.destroy()
        self.match_vars=[]
        self.choice_var.set("")

    def _show_text_entry(self):
        self._clear_dynamic()
        self.text_answer=tk.Text(
            self.dynamic,height=8,wrap="word",bg="#f5f9fd",fg="#10233f",
            insertbackground="#10233f",relief="flat",
            font=("Helvetica",12),padx=10,pady=10
        )
        self.text_answer.pack(fill="both",expand=True)
        self.text_answer.bind("<KeyRelease>",self._update_reveal_state)

    def _make_response_ui(self):
        self._clear_dynamic()
        if not self.current:
            self._show_text_entry()
            return

        t=self.current["type"]
        if t in ("definition","explanation","scenario","fill_blank"):
            self._show_text_entry()

        elif t=="multiple_choice":
            self.choice_var=tk.StringVar(value="")
            choices=list(self.current["choices"])
            random.shuffle(choices)
            for choice in choices:
                rb=ttk.Radiobutton(
                    self.dynamic,text=choice,value=choice,
                    variable=self.choice_var,style="Choice.TRadiobutton",
                    command=self._update_reveal_state
                )
                rb.pack(anchor="w",fill="x",pady=4)

        elif t=="matching":
            items=list(self.current["match_items"])
            right=[b for _,b in items]
            random.shuffle(right)

            ttk.Label(
                self.dynamic,
                text="Match each term on the left to one description on the right.",
                style="QuestionType.TLabel"
            ).pack(anchor="w",pady=(0,8))

            descriptions={chr(65+i):desc for i,desc in enumerate(right)}
            for letter,desc in descriptions.items():
                ttk.Label(
                    self.dynamic,text=f"{letter}. {desc}",
                    style="QuestionType.TLabel",wraplength=730,justify="left"
                ).pack(anchor="w",pady=1)

            ttk.Separator(self.dynamic).pack(fill="x",pady=8)

            for term,_ in items:
                row=ttk.Frame(self.dynamic,style="Card.TFrame")
                row.pack(fill="x",pady=3)
                ttk.Label(row,text=term,style="QuestionType.TLabel",width=24).pack(side="left")
                var=tk.StringVar(value="")
                self.match_vars.append((term,var,descriptions))
                combo=ttk.Combobox(
                    row,textvariable=var,
                    values=list(descriptions.keys()),
                    state="readonly",width=6
                )
                combo.pack(side="left")
                combo.bind("<<ComboboxSelected>>",self._update_reveal_state)

        self._update_reveal_state()

    def _attempt_made(self):
        if not self.current:
            return False
        t=self.current["type"]
        if t in ("definition","explanation","scenario"):
            return len(self.text_answer.get("1.0","end").strip()) >= 12
        if t=="fill_blank":
            return len(self.text_answer.get("1.0","end").strip()) >= 2
        if t=="multiple_choice":
            return bool(self.choice_var.get())
        if t=="matching":
            return bool(self.match_vars) and all(v.get() for _,v,_ in self.match_vars)
        return False

    def _update_reveal_state(self,event=None):
        self.reveal_btn.config(state="normal" if self._attempt_made() else "disabled")

    def _normalize(self,s):
        return re.sub(r"[^a-z0-9]+"," ",s.lower()).strip()

    def _objective_result(self):
        if not self.current:
            return None
        t=self.current["type"]

        if t=="fill_blank":
            user=self._normalize(self.text_answer.get("1.0","end"))
            accepted=[self._normalize(self.current["answer"])] + [
                self._normalize(x) for x in self.current["aliases"]
            ]
            return user in accepted

        if t=="multiple_choice":
            return self.choice_var.get()==self.current["correct"]

        if t=="matching":
            expected=dict(self.current["match_items"])
            for term,var,descriptions in self.match_vars:
                chosen_desc=descriptions.get(var.get())
                if chosen_desc != expected[term]:
                    return False
            return True

        return None

    def reveal(self):
        if not self.current:
            return
        if not self._attempt_made():
            messagebox.showinfo("Answer First","Make an attempt before revealing the sample answer.")
            return

        result=self._objective_result()
        if result is not None:
            self.objective_attempted += 1
            if result:
                self.objective_correct += 1
                verdict="Your objective answer matches the key."
            else:
                verdict="Your objective answer does not match the key."
            self.score_label.config(
                text=f"Session score: {self.objective_correct} / {self.objective_attempted}"
            )
        else:
            verdict="Compare your explanation with the sample rather than looking for exact wording."

        text=(
            f"{verdict}\n\n"
            f"Sample answer:\n{self.current['answer']}\n\n"
            f"Why it matters:\n{self.current['explanation']}"
        )
        self.answer_label.config(text=text)
        self.answer_frame.pack(fill="x",pady=(10,0))
        self.reveal_btn.config(state="disabled")
        self.status.config(text="Review the key points, then generate another question.")

    def clear_response(self):
        self.answer_frame.pack_forget()
        if not self.current:
            self._show_text_entry()
            self.reveal_btn.config(state="disabled")
            return
        self._make_response_ui()
        self.reveal_btn.config(state="disabled")

    def reset_session(self):
        self.session_seen.clear()
        self.objective_attempted=0
        self.objective_correct=0
        self.score_label.config(text="Session score: 0 / 0")
        self.current=None
        self.meta_label.config(text="")
        self.question_label.config(text="Click Generate Question to begin.")
        self.helper_label.config(text="")
        self.pool_label.config(text="")
        self.art.draw("shield")
        self.answer_frame.pack_forget()
        self._show_text_entry()
        self.reveal_btn.config(state="disabled")
        self.status.config(text="Session reset. Generate a question when ready.")

if __name__ == "__main__":
    QuizApp().mainloop()
