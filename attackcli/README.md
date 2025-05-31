# 🛠️ HTTP Strike Kit

A command-line toolkit for simulating common web-layer and network-layer attacks.

---

## 🚀 Getting Started

Run this from a container named `attackcli`.  
To explore available commands:

```shell
attack --help
```

---

## Available Attack Methods

### 🔐 Brute Force Attack

Attempts to brute-force common login endpoints by trying multiple paths from a wordlist.

> Important Note ! using `host.docker.internal` inside the container, running it in host it's of course `localhost`

```shell
attack brute-force -u host.docker.internal:80 -w path/to/wordlists -t 10
```

---

### 🦥 Slowloris Attack

Exploits HTTP/1.x by opening multiple connections and sending partial requests slowly to exhaust the server’s resources.

```shell
attack slowloris -t host.docker.internal -p 80
```

---

### 🌊 SYN Flood Attack

Sends a flood of TCP SYN packets to exhaust server-side resources and simulate a Denial-of-Service condition.

```shell
attack syn-flood -t host.docker.internal -p 80
```