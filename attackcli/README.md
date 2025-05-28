# 🛠️ HTTP Strike Kit

A command-line toolkit for simulating common web-layer and network-layer attacks.

---

## 🚀 Getting Started

You can run this in the terminal or in a container.  
Note that for using in a container you need to uncomment it in
`docker-compose.yaml`.  
(I don't really see a reason to put this in container, but you asked for it xd)
To explore available commands:

```shell
cli.py --help             # View general help information
cli.py attack --help      # View available attack types and options
```

---

## 💣 Available Attack Methods

### 🔐 Brute Force Attack

Attempts to brute-force common login endpoints by trying multiple paths or credentials from a wordlist.

```shell
cli.py attack brute-force -u http://localhost:8000/ -w path/to/wordlists -t 10
```

---

### 🐌 Slowloris Attack

Exploits HTTP/1.x by opening multiple connections and sending partial requests slowly to exhaust the server’s resources.

```shell
cli.py attack slowloris -t 127.0.0.1 -p 8000
```

---

### 🌊 SYN Flood Attack

Sends a flood of TCP SYN packets to exhaust server-side resources and simulate a Denial-of-Service condition.

```shell
cli.py attack syn-flood -t 127.0.0.1 -p 8000
```