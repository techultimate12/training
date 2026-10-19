#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import random

APP_TITLE = "Entry-Level IT Interview Practice"

QUESTIONS = []
def add(cat, q, a, tip=""):
    QUESTIONS.append({"category":cat,"question":q,"answer":a,"tip":tip})

# Behavioral questions
behavioral = [
("Tell me about a time you had to learn a new technology quickly.","Use STAR. Explain what you needed to learn, how you approached it, how you practiced, and the result. A good entry-level example could be learning PowerShell, a ticketing tool, Linux commands, or networking basics for a class or project."),
("Tell me about a time you made a mistake and how you handled it.","Take responsibility, explain how you corrected it, and describe what you changed so the mistake would not happen again."),
("Describe a time you had multiple priorities at once.","Explain how you ranked tasks by urgency and impact, communicated expectations, tracked your work, and completed the highest-priority items first."),
("Tell me about a time you helped someone who was frustrated.","Show patience, active listening, simple communication, and follow-up. In IT, user experience matters along with the technical fix."),
("Tell me about a time you worked with someone who had a different working style.","Describe how you adapted communication, clarified responsibilities, and focused on the shared goal."),
("Describe a time you solved a problem without having all the information.","Explain how you gathered facts, formed hypotheses, tested safely, documented results, and asked for help when appropriate."),
("Tell me about a time you received critical feedback.","Show that you listened, asked questions, made a change, and improved rather than becoming defensive."),
("Tell me about a time you explained something technical to a nontechnical person.","Use plain language, avoid unnecessary jargon, use an analogy if helpful, and check for understanding."),
("Describe a time you had to follow a process you did not fully agree with.","Explain that you followed the approved process while raising concerns through the proper channel."),
("Tell me about a time you took initiative.","Give an example of a useful improvement you noticed and completed, such as documentation, a checklist, automation, or better organization."),
("Tell me about a time you had to ask for help.","Show that you first made a reasonable effort, gathered useful details, then asked a focused question or escalated."),
("Describe a time you had to stay calm under pressure.","Explain how you focused on facts, handled the most important issue first, communicated status, and avoided rushed changes."),
("Tell me about a time you disagreed with a teammate.","Describe respectful communication, listening, evidence-based discussion, and reaching a workable solution."),
("Describe a situation where documentation helped you.","Explain how a checklist, notes, or knowledge base reduced errors, saved time, or helped someone else."),
("Tell me about a time you improved a repetitive task.","Describe a simple improvement such as a template, shortcut, checklist, or script that saved time or reduced mistakes."),
("Why do you want to work in IT?","Connect technology with problem-solving, helping users, continuous learning, and building practical skills."),
("Why are you interested in an entry-level IT role?","Explain that you want hands-on experience with users, hardware, software, networks, and troubleshooting while building a strong foundation."),
("What does good customer service mean in IT?","Listening, clear communication, realistic expectations, protecting data, efficient troubleshooting, and follow-up."),
("How do you handle a problem you have never seen before?","Gather symptoms and scope, check recent changes, consult documentation, test low-risk fixes one at a time, document results, and escalate when appropriate."),
("How do you stay organized?","Mention ticket queues, task lists, calendars, notes, priorities, and documenting next actions.")
]
for q,a in behavioral:
    add("Behavioral", q, a, "Use STAR: Situation, Task, Action, Result.")

# General IT fundamentals
it_bank = [
("What is the difference between RAM and storage?","RAM is temporary working memory used while programs run. Storage such as an SSD retains files and applications when power is off."),
("What is an IP address?","An IP address identifies a device on an IP network so traffic can be routed to and from it."),
("What is DNS?","DNS translates human-readable names such as example.com into IP addresses."),
("What is DHCP?","DHCP automatically assigns network settings such as IP address, subnet mask, gateway, and DNS servers."),
("What is a default gateway?","The default gateway is the router a device uses to reach destinations outside its local network."),
("What is a subnet mask?","A subnet mask helps identify which part of an IPv4 address is the network portion and which part is the host portion."),
("What is the difference between a switch and a router?","A switch connects devices on a local network. A router connects different IP networks and forwards packets between them."),
("What is the difference between HTTP and HTTPS?","HTTPS is HTTP protected by TLS encryption and server authentication."),
("What is a VPN?","A VPN creates an encrypted tunnel between a device and a VPN endpoint, often for secure remote access."),
("What is the purpose of an operating system?","It manages hardware, memory, processes, files, devices, security, and application access to system resources."),
("What is Active Directory?","Microsoft Active Directory centrally manages users, computers, groups, authentication, and policies."),
("What is Group Policy?","Group Policy lets administrators centrally apply Windows configuration and security settings."),
("What is virtualization?","Virtualization allows multiple virtual machines to share the hardware of one physical host."),
("What is a virtual machine?","A virtual machine is a software-based computer with virtual CPU, memory, storage, and networking."),
("What is cloud computing?","Cloud computing provides on-demand computing resources such as servers, storage, and applications over a network."),
("What is SaaS?","Software as a Service is software delivered as a hosted service, often accessed by browser or client application."),
("What is a device driver?","A driver lets an operating system communicate with a hardware device."),
("What is firmware?","Firmware is low-level software stored on hardware that controls basic device behavior."),
("What is BIOS or UEFI?","BIOS/UEFI initializes hardware and starts the operating system boot process. UEFI is the modern standard."),
("What is a process?","A process is a running instance of a program with allocated resources."),
("What is a service?","A service is a background process that provides a system or application function."),
("What is ping used for?","Ping uses ICMP to test reachability and response time. Failure does not always mean the host is down because ICMP can be blocked."),
("What does ipconfig help you check on Windows?","It displays network adapter details including IP address, gateway, and other network configuration."),
("What is Task Manager used for?","It helps inspect running processes and CPU, memory, disk, and network usage."),
("What is an SSD?","An SSD stores data using flash memory and is generally much faster than a traditional hard drive."),
("What is the difference between 2.4 GHz and 5 GHz Wi-Fi?","2.4 GHz generally reaches farther but is more crowded; 5 GHz generally supports higher speeds over shorter distances."),
("What is latency?","Latency is the delay between sending data and receiving a response."),
("What is bandwidth?","Bandwidth is the amount of data a connection can carry in a given period."),
("What is a MAC address?","A MAC address is a link-layer identifier assigned to a network interface."),
("What is the difference between TCP and UDP?","TCP is connection-oriented and provides reliable ordered delivery. UDP is connectionless and lower overhead but does not guarantee delivery."),
("What is a port number?","A port number identifies a network service or application endpoint on a host."),
("What does localhost mean?","Localhost refers to the same computer, commonly using 127.0.0.1 for IPv4."),
("What is a domain name?","A domain name is a human-readable name that DNS can map to network resources."),
("What is an administrator account?","An administrator account has elevated permissions to make system-level changes."),
("What is least privilege in IT administration?","Users should receive only the permissions required to perform their work."),
]
for q,a in it_bank:
    add("General IT",q,a,"Explain it simply, as if speaking to a user.")

# Troubleshooting fundamentals
trouble = [
("A user says, 'My computer is slow.' What do you do first?","Ask when it started, whether one app or everything is slow, and whether there were recent changes. Then check CPU, memory, disk, free space, startup programs, updates, and network conditions."),
("A computer will not power on. What would you check?","Verify outlet, cable, adapter, power strip, battery, and visible indicators. Try known-good power components when appropriate before escalating hardware diagnosis."),
("A user cannot connect to Wi-Fi. How would you troubleshoot?","Check Wi-Fi state, airplane mode, correct network, signal strength, whether other devices work, adapter status, IP configuration, and whether the issue is device-specific."),
("A user can reach a website by IP address but not by name. What does that suggest?","It strongly suggests a DNS issue. Check DNS configuration, test name resolution, and verify the DNS server is reachable."),
("A printer shows offline. What do you check?","Check power, connection, printer display errors, paper/toner, correct queue, print jobs, and whether other users can print."),
("A user cannot log in. What do you ask?","Ask for the exact error, verify username, caps lock, account status, network connectivity, and whether the user can sign in elsewhere."),
("An application keeps crashing. What do you do?","Capture the exact error, reproduce the issue, check scope, recent changes, system resources and logs, then try approved repair/update steps."),
("A monitor is blank but the computer is running. What do you check?","Check monitor power, brightness, input source, cable, docking station, display settings, and a known-good monitor or cable."),
("A microphone does not work in a video call. What do you check?","Check mute, selected input device, OS/app permissions, connection, input level, and whether it works in another application."),
("A user says the internet is down. What is your first goal?","Determine scope: one device, one user, one area, or everyone. Scope tells you where to troubleshoot."),
("A laptop is overheating. What would you check?","Check airflow, fans, dust, CPU load, background processes, surface placement, and power settings."),
("A USB device is not recognized. What do you try?","Reconnect it, try another port, test it on another device if safe, inspect driver/device status, and try a known-good device."),
("A user has no sound. What do you check?","Check mute/volume, selected output device, Bluetooth or cable connection, app-specific volume, and driver status."),
("A user's storage is almost full. What do you do?","Identify what uses space, remove safe temporary files, archive approved data, and avoid deleting unknown files."),
("A shared network drive is unavailable to one user. What do you check?","Check network/VPN connectivity, path, permissions, credentials, and whether other users can access it."),
("A user can receive email but cannot send it. What do you check?","Check errors, outbox, connectivity, mailbox limits, account status, and whether webmail can send."),
("A system is at 100% CPU. What do you do?","Identify the process consuming CPU, determine whether it is expected, check recent changes, and avoid terminating critical processes without understanding them."),
("A user deleted an important file. What do you do?","Check recycle/trash, backups, cloud version history, and approved recovery procedures while avoiding unnecessary disk writes."),
("A problem returns the next day after you fixed it. What do you do differently?","Investigate root cause using logs, patterns, recent changes, dependencies, and documentation rather than repeating only the workaround."),
("When should an entry-level technician escalate?","Escalate when the issue exceeds your permissions or skill, affects critical/multiple systems, involves security, requires risky changes, or remains unresolved after reasonable documented troubleshooting.")
]
for q,a in trouble:
    add("Troubleshooting",q,a,"Think: scope → facts → safe test → verify → document → escalate.")

# Security fundamentals
sec = [
("What is the CIA triad?","Confidentiality limits access to authorized users, Integrity protects accuracy and trustworthiness, and Availability keeps systems and data accessible when needed."),
("What is phishing?","Phishing is social engineering that tries to trick users into revealing information, clicking malicious links, or opening harmful files."),
("What is multi-factor authentication?","MFA requires more than one authentication factor, such as something you know, have, or are."),
("Why are software patches important?","Patches fix vulnerabilities, bugs, and reliability issues. Delays can leave known weaknesses exposed."),
("What is least privilege?","Give users and systems only the permissions needed to perform their jobs."),
("What makes a good password policy?","Long unique passwords or passphrases, no reuse, blocking known-compromised passwords, and MFA."),
("What is malware?","Malware is malicious software designed to harm, disrupt, spy on, steal from, or gain unauthorized access to systems."),
("What is ransomware?","Ransomware is malware that encrypts or blocks access to systems or data and demands payment."),
("What is endpoint protection?","Endpoint protection monitors devices for malicious files, behavior, processes, and indicators of compromise."),
("What is a firewall?","A firewall allows or blocks network traffic based on configured rules."),
("What is social engineering?","Social engineering manipulates people into bypassing security controls or revealing sensitive information."),
("What is encryption?","Encryption converts readable data into ciphertext that requires a key to decrypt."),
("What is hashing?","Hashing creates a one-way fixed-size digest commonly used for integrity checks and password storage systems."),
("What is the difference between authentication and authorization?","Authentication verifies identity; authorization determines what that identity is allowed to do."),
("What is a vulnerability?","A vulnerability is a weakness in software, hardware, configuration, or process that could be exploited."),
("What is a threat?","A threat is something capable of causing harm, such as an attacker, malware, or insider misuse."),
("What is risk?","Risk is the potential harm when a threat can exploit a vulnerability, often evaluated by likelihood and impact."),
("What is a security incident?","A security incident is an event that threatens or violates confidentiality, integrity, availability, or security policy."),
("Why should users lock their screens?","It prevents unauthorized access when they step away from the device."),
("Why is password reuse dangerous?","A breach at one service can let attackers try the same credentials against other services."),
("What is a password manager?","A password manager securely stores and generates unique credentials."),
("What is shoulder surfing?","Observing someone's screen or keyboard to capture sensitive information."),
("What is tailgating?","Following an authorized person into a restricted physical area without proper authentication."),
("Why are backups important for security?","They support recovery from ransomware, accidental deletion, hardware failure, and other incidents."),
("What is defense in depth?","Using multiple security layers so one failed control does not expose everything."),
("What is EDR?","Endpoint Detection and Response monitors endpoint behavior and supports detection, investigation, and response."),
("What is a security log?","A security log records events such as logins, process activity, network activity, and configuration changes."),
("Why should default passwords be changed?","Default credentials are widely known and commonly targeted."),
("Why is public Wi-Fi risky?","It is untrusted and may expose users to malicious hotspots, spoofing, or interception attempts."),
("What is the purpose of a security policy?","It defines approved behavior, responsibilities, controls, and procedures for protecting systems and information.")
]
for q,a in sec:
    add("Cybersecurity Fundamentals",q,a,"Define the concept and explain why it matters.")

# Security scenarios
scenarios = [
("A user forwards you an email saying, 'This looks suspicious.' What do you do?","Do not click links or open attachments. Preserve/report the message using approved tools and advise the user not to interact with it. Escalate if they entered credentials or opened anything."),
("A user clicked a suspicious link but says they did not enter a password. What next?","Gather details and time, follow the incident process, inspect browser/download activity with approved tools, isolate if policy requires, and document the event."),
("A user entered their password on a suspected phishing page. What should happen?","Reset the password promptly, revoke active sessions if possible, verify MFA, review sign-in activity, and notify security."),
("You find a USB drive in the parking lot. What do you do?","Do not plug it into a company system. Turn it over to security or IT according to policy."),
("Someone calls claiming to be the CEO and urgently asks you to reset their password. What do you do?","Follow normal identity-verification procedures regardless of title or urgency. Never bypass controls because someone pressures you."),
("A user asks you to disable antivirus because it blocks a download. What do you do?","Do not disable protection just to make the download work. Verify the source and use the approved exception/escalation process."),
("You see repeated failed login attempts on an account. What do you do?","Verify whether they are legitimate, review available source/timing information, confirm with the user, and escalate suspicious activity."),
("A user wants permanent local administrator rights for convenience. What do you say?","Follow least privilege and the approved software/elevation process rather than granting unnecessary permanent admin access."),
("A screen suddenly displays a ransomware demand. What do you do?","Isolate the device if it can be done safely and policy supports it, do not interact with the ransom note, preserve evidence, and notify security immediately."),
("A user receives an MFA prompt they did not initiate. What do you tell them?","Deny it, do not approve it, verify recent sign-ins, change credentials if compromise is suspected, and report it."),
("A coworker asks to use your account because theirs is locked. What do you do?","Do not share credentials or allow them to work under your account. Help them restore their own access through the proper process."),
("A company laptop is lost. What should happen?","Report it immediately, provide last-known details, trigger approved remote lock/wipe actions if available, review account access, and follow incident procedures."),
("A user sends company data to personal email to work from home. What is the concern?","It may bypass approved security controls and violate data-handling policy. Use approved remote-access or file-sharing systems."),
("An employee leaves the company. What access steps matter?","Disable accounts, revoke sessions/tokens, recover devices, remove groups and application access, and document completion."),
("You are asked to email a password in plain text. What do you do?","Use an approved reset or secure secret-sharing process instead of plain-text email."),
("A visitor is walking around a restricted office without a badge. What do you do?","Follow physical-security procedures: politely challenge if appropriate or notify security."),
("A user says they clicked 'Allow' on an antivirus warning. What do you do?","Treat it as a potential event, gather details, inspect endpoint alerts using approved tools, isolate if required, and escalate."),
("A shared folder gives everyone full control. What is the problem?","It violates least privilege and increases the risk of accidental or malicious changes. Determine required access and correct it through an approved change."),
("You see credentials on a sticky note attached to a monitor. What do you do?","Address it discreetly, have the note removed, encourage an approved password manager, and follow policy if exposure occurred."),
("A browser shows a certificate warning on a company website. Should the user click through?","No. Stop and verify the URL/certificate issue with IT because the warning may indicate misconfiguration or interception."),
("A user receives a phone call asking for their MFA code. What do you tell them?","Never share MFA codes. Treat the request as social engineering and report it."),
("An unknown device appears on the company network. What do you do?","Gather identifying information, verify whether it is authorized, avoid destroying evidence, and notify networking/security."),
("A user's email is automatically forwarding to an unknown address. What might that mean?","Possible account compromise. Remove unauthorized rules, reset credentials, revoke sessions, review sign-ins, and report it."),
("A workstation starts contacting many unfamiliar external IP addresses. What do you do?","Treat it as suspicious, isolate according to policy, gather endpoint/network evidence, and escalate to security."),
("A user receives an unexpected password-reset email. What should they do?","Do not use the message link. Go directly to the known service, verify account activity, and report the message if suspicious.")
]
for q,a in scenarios:
    add("Security Scenarios",q,a,"Protect first, preserve evidence, follow policy, and escalate.")

# Generate many additional realistic variations
devices = ["Windows laptop","MacBook","desktop PC","shared workstation","conference-room computer","remote employee laptop"]
symptoms = [
("cannot reach any websites","check link/Wi-Fi, scope, IP settings, gateway, DNS, and whether other devices are affected"),
("can browse the web but cannot reach a company file share","check VPN/internal connectivity, path, credentials, permissions, and whether others can reach the share"),
("takes several minutes to sign in","check network/domain connectivity, startup items, resource usage, free storage, and recent changes"),
("loses network connection every few minutes","check signal/cable stability, adapter status, logs, power settings, and whether the issue follows the device"),
("cannot print to the office printer","check printer reachability, queue, permissions, spooler, and whether other users can print"),
("shows very high disk usage","identify the process causing disk activity, free space, updates, scans, and drive health indicators"),
("has a Bluetooth headset that will not connect","check power, pairing mode, previous pairings, Bluetooth state, and selected audio device"),
("cannot join a video meeting","check connectivity, application status, permissions, account access, audio/video devices, and service status"),
]
for d in devices:
    for symptom, checks in symptoms:
        add("Troubleshooting",
            f"A user says their {d} {symptom}. Walk me through your troubleshooting approach.",
            f"Clarify when it started, whether it happens every time, and who else is affected. Then isolate the issue with low-risk tests: {checks}. Make one change at a time, verify the fix, explain the result to the user, and document what you did.",
            "Interviewers care more about your process than memorizing one fix.")

assets = ["employee laptop","shared kiosk","cloud account","email account","file server","Wi-Fi network","administrator account"]
alerts = [
("shows an unexpected MFA prompt","deny it, verify sign-in activity, protect credentials, and report the event"),
("receives a suspicious attachment","do not open it, preserve/report it, and inspect only with approved tools"),
("appears to have an unknown administrator account","verify authorization, preserve evidence, isolate if required, and escalate"),
("is suddenly sending spam","treat it as possible compromise, protect the account, inspect logs, and notify security"),
("has an unknown remote-access tool installed","verify authorization, preserve evidence, isolate if suspicious, and escalate"),
("is connecting to a suspicious domain","identify the involved process/device, contain through approved controls, and investigate with security"),
]
for asset in assets:
    for alert, action in alerts:
        add("Security Scenarios",
            f"You discover that an {asset} {alert}. What would you do as an entry-level IT technician?",
            f"Treat it as a potential security event rather than an ordinary support issue. Confirm the basic facts without making destructive changes. Generally you would {action}. Record times, symptoms, users involved, and actions taken, then follow the organization's incident-response process.",
            "Do not try to be the hero; correct escalation is a strength.")

behaviors = [
"meeting a tight deadline","working as part of a team","communicating a difficult idea",
"adjusting when requirements changed","keeping track of several tasks","helping someone who was upset",
"learning something outside your comfort zone","catching an error before it caused a bigger problem",
"improving something without being asked","sticking with a difficult problem","working with limited instructions",
"handling a task that did not go as planned","supporting a teammate","organizing a project","learning from failure"
]
for b in behaviors:
    add("Behavioral",
        f"Give me an example of {b}. What did you do and what was the outcome?",
        "Use STAR. Briefly describe the situation and your responsibility, spend most of the answer on the specific actions you personally took, then finish with the result and what you learned.",
        "Aim for a 60–90 second answer.")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1180x760")
        self.minsize(980,680)
        self.configure(bg="#06142d")
        self.current=None
        self._styles()

        root=ttk.Frame(self,style="Main.TFrame",padding=20)
        root.pack(fill="both",expand=True)

        head=ttk.Frame(root,style="Header.TFrame",padding=16)
        head.pack(fill="x",pady=(0,14))
        ttk.Label(head,text="Entry-Level IT Interview Practice",style="Title.TLabel").pack(anchor="w")
        ttk.Label(head,text=f"{len(QUESTIONS)} randomized practice questions • Behavior • IT • Troubleshooting • Cybersecurity",style="Subtitle.TLabel").pack(anchor="w",pady=(4,0))

        ctr=ttk.Frame(root,style="Main.TFrame")
        ctr.pack(fill="x",pady=(0,12))
        ttk.Label(ctr,text="Category:",style="Main.TLabel").pack(side="left")
        self.cat=tk.StringVar(value="All Categories")
        cats=["All Categories"]+sorted({x["category"] for x in QUESTIONS})
        ttk.Combobox(ctr,textvariable=self.cat,values=cats,state="readonly",width=28).pack(side="left",padx=10)
        ttk.Button(ctr,text="Generate Question",command=self.generate,style="Accent.TButton").pack(side="left")
        self.count=ttk.Label(ctr,text="",style="Main.TLabel")
        self.count.pack(side="right")

        qbox=ttk.LabelFrame(root,text=" Interview Question ",style="Card.TLabelframe",padding=18)
        qbox.pack(fill="x",pady=(0,12))
        self.catlabel=ttk.Label(qbox,text="",style="Category.TLabel"); self.catlabel.pack(anchor="w")
        self.qlabel=ttk.Label(qbox,text="Click Generate Question to begin.",style="Question.TLabel",wraplength=1080,justify="left")
        self.qlabel.pack(fill="x",pady=(8,4))
        self.tip=ttk.Label(qbox,text="",style="Tip.TLabel",wraplength=1080,justify="left")
        self.tip.pack(fill="x")

        abox=ttk.LabelFrame(root,text=" Your Best Effort ",style="Card.TLabelframe",padding=14)
        abox.pack(fill="both",expand=True,pady=(0,12))
        ttk.Label(abox,text="Type your answer first. The example-answer button unlocks after you enter an attempt.",style="CardBody.TLabel").pack(anchor="w",pady=(0,7))
        self.attempt=tk.Text(abox,height=7,wrap="word",bg="#f5f8fc",fg="#10233f",insertbackground="#10233f",relief="flat",font=("Helvetica",12),padx=10,pady=10)
        self.attempt.pack(fill="both",expand=True)
        self.attempt.bind("<KeyRelease>",self.check_attempt)

        buttons=ttk.Frame(root,style="Main.TFrame"); buttons.pack(fill="x")
        self.reveal=ttk.Button(buttons,text="Reveal Example Answer",command=self.show_answer,state="disabled",style="Secondary.TButton")
        self.reveal.pack(side="left")
        ttk.Button(buttons,text="Clear My Answer",command=self.clear,style="Secondary.TButton").pack(side="left",padx=10)

        self.answerbox=ttk.LabelFrame(root,text=" Example Answer / Key Points ",style="Answer.TLabelframe",padding=16)
        self.alabel=ttk.Label(self.answerbox,text="",style="Answer.TLabel",wraplength=1080,justify="left")
        self.alabel.pack(fill="x")

        self.status=ttk.Label(root,text="Tip: say your answer out loud before typing it for more realistic practice.",style="Footer.TLabel")
        self.status.pack(anchor="w",pady=(10,0))

    def _styles(self):
        s=ttk.Style(self)
        try:s.theme_use("clam")
        except:pass
        bg="#06142d"; panel="#0b2247"; panel2="#0f2f60"; text="#eef7ff"; muted="#a8c8e8"
        s.configure("Main.TFrame",background=bg)
        s.configure("Header.TFrame",background=panel)
        s.configure("Main.TLabel",background=bg,foreground=text,font=("Helvetica",11))
        s.configure("CardBody.TLabel",background=panel2,foreground=text,font=("Helvetica",11))
        s.configure("Title.TLabel",background=panel,foreground="white",font=("Helvetica",24,"bold"))
        s.configure("Subtitle.TLabel",background=panel,foreground=muted,font=("Helvetica",11))
        s.configure("Category.TLabel",background=panel2,foreground="#73c4ff",font=("Helvetica",11,"bold"))
        s.configure("Question.TLabel",background=panel2,foreground="white",font=("Helvetica",18,"bold"))
        s.configure("Tip.TLabel",background=panel2,foreground="#b9dbf5",font=("Helvetica",10,"italic"))
        s.configure("Footer.TLabel",background=bg,foreground=muted,font=("Helvetica",10))
        s.configure("Card.TLabelframe",background=panel2,foreground="white")
        s.configure("Card.TLabelframe.Label",background=panel2,foreground="#8bd2ff",font=("Helvetica",11,"bold"))
        s.configure("Answer.TLabelframe",background="#10294d",foreground="white")
        s.configure("Answer.TLabelframe.Label",background="#10294d",foreground="#82e6b5",font=("Helvetica",11,"bold"))
        s.configure("Answer.TLabel",background="#10294d",foreground="#eef7ff",font=("Helvetica",12))
        s.configure("Accent.TButton",background="#1c91ff",foreground="white",padding=(16,9),font=("Helvetica",11,"bold"))
        s.map("Accent.TButton",background=[("active","#38a5ff")])
        s.configure("Secondary.TButton",background="#173d73",foreground="white",padding=(14,8),font=("Helvetica",10,"bold"))
        s.map("Secondary.TButton",background=[("active","#24548f"),("disabled","#26384f")],foreground=[("disabled","#8291a5")])
        s.configure("TCombobox",fieldbackground="#f4f8fc",foreground="#0a1c34",padding=6)

    def generate(self):
        cat=self.cat.get()
        pool=QUESTIONS if cat=="All Categories" else [q for q in QUESTIONS if q["category"]==cat]
        if self.current and len(pool)>1:
            pool2=[q for q in pool if q is not self.current]
            self.current=random.choice(pool2 or pool)
        else:self.current=random.choice(pool)
        self.catlabel.config(text=self.current["category"])
        self.qlabel.config(text=self.current["question"])
        self.tip.config(text="Interview tip: "+self.current["tip"] if self.current["tip"] else "")
        self.count.config(text=f"{len(pool)} questions available")
        self.clear()
        self.status.config(text="Give your best answer first, then reveal the example.")

    def check_attempt(self,event=None):
        text=self.attempt.get("1.0","end").strip()
        self.reveal.config(state="normal" if self.current and len(text)>=15 else "disabled")

    def show_answer(self):
        if not self.current:return
        if len(self.attempt.get("1.0","end").strip())<15:
            messagebox.showinfo("Try First","Enter a short attempt before revealing the example answer.")
            return
        self.alabel.config(text=self.current["answer"])
        self.answerbox.pack(fill="x",before=self.status,pady=(10,0))
        self.status.config(text="Compare the structure and key points—not exact wording. Your answer should still sound like you.")

    def clear(self):
        self.attempt.delete("1.0","end")
        self.reveal.config(state="disabled")
        self.answerbox.pack_forget()

if __name__=="__main__":
    App().mainloop()
