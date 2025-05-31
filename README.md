# Reverse Proxy Game

## Pick a team and defeat your opponent!

### 🔴 Red Team

Develop an `attack cli` and attack the `webserver`.  
Your goal is to put him down! 😈

### 🔵 Blue Team

Configure nginx to defend the `webserver`.  
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

### Nginx

You can edit the configuration here: [nginx.conf](nginx/nginx.conf).

###### All requests to the web server go through this proxy first.

### Tools to play with 🧸

#### Adminer

Connect to adminer to see data from the webserver db.  
Connection details:

```dotenv
System: PostgreSQL
Server: webserver-postgres
Username: admin
Password: admin
Database: db
```

#### Kibana

Connect to kibana to see webserver logs.

First, we need to import our data views so we can see the logs in a discovery section, so let's do this.

###### Make sure the path to `kibana-data-views.ndjson` is correct.

```shell
curl -X POST http://localhost:5601/api/saved_objects/_import -H "kbn-xsrf: true" --form file=@./kibana/kibana-data-views.ndjson
```

Now go to [kibana](http://localhost:5601/app/discover).   
There are three indexes:

- `infra-logs` - to log webserver actions.
- `user-actions` - to log user actions in the webserver.
- `nginx-logs` - to keep all nginx logs.

# NOTES

### General Notes

I loaded configuration files that have sensitive data. And I'm aware of that, but for the sake of the exercise I put
them
here.

We can't stop SYN Flood attack using nginx. You need to take care of it in the kernel level.  
You need to set tcp syn cookies and reduce tcp syn ack retry time.  
You can also increase the pending connections pool. You can also limit it in iptables.  
These things can be configured on the hosting server but not in dockers.  

I limited connections with nginx, and I hope this passes :)