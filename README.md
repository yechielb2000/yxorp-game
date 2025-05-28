# Reverse Proxy Game

## Pick a team and defeat your opponent!

### 🔴 Red Team

Develop an `attack cli` and attack the `webserver`.  
Your goal is to put him down! 😈

### 🔵 Blue Team

Develop a `proxy server` to defend the `webserver`.  
Your mission is to protect it at all costs! 💂

There are already usable components, but they don't do much since the attacks are useless against the proxy
defense!

## Get to know your components

The components were developed in the same repo.  
I attached them to one repo but in different environments. This is why you see the directories twice.   
I don't usually do this, I wanted to keep in one GitHub project.  
You can, of course, split them into separated projects.

### Web Server (The target)

Webserver for geolocation queries.  
[README.md](webserver/README.md)

### Attack CLI

CLI to attach http servers.  
[README.md](attackcli/README.md)

### Proxy Server

A proxy server to stop the attackers.  
All requests to the web server go through this proxy first.