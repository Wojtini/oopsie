# Oopsie
Ansible's playbooks and roles for my own personal homelab.

# Roles:
## docker
Install docker on target system. Used as dependency for other roles that uses docker to deploy services.

## nginx_rp
Nginx is used as reverse proxy for exposed services.
nginx.conf template should be manually modified in order to deploy new service.

Additionally, letsencrypt's certbot is used for automatic certificate generation
for domains defined in subdomains dict.

### variables
```
# mail for [letsencrypt](https://letsencrypt.org/docs/expiration-emails/) used for sending an expiration notice.
letsencrypt_email: name@mail.com

# Registered primary domain name
domain_name: test.xyz

# Dict for storing registered subdomains.
subdomains:
  example:  # service name (not used by any task)
    prefix: example.    # (required) prefix for primary domain name, used for certs generation
    ...                 # (optional) more vals which may be handy in nginx.conf. Example: upstream server
```

## Monitoring roles:
### Grafana

```
### Desired grafana docker image
grafana_image: grafana/grafana-enterprise:11.1.0-boringcrypto

### Desired port (both internal and external)
grafana_port: 3000

### Configured datasources, its copy pasted into grafana config.
datasources:
  - name: Prometheus
    type: prometheus
    url: http://localhost:9090
    isDefault: true
    access: proxy
    editable: true

compose_location: /home/grafana

```


### Prometheus
no settings yet
### node_exporter
no settings yet

## minecraft_server

### Variables
```
### server jar file needs to be manually added for playbook to be copied
server_jar_file: server.jar

### java, make sure it is compatible with provided jar file
java_apt_package: openjdk-21-jdk

### server_settings overwrite default server.properties values
server_settings:
    motd: "A new motd"
```


## Jenkins
CI/CD tool for internal and personal automation.
Currently, it also creates backups for other systems.

Port 50000 needs to be opened for inbound agents
### Jenkins agents
Deployment of inbound agents.
Example:
```
nodes:
    agent_1:                        # used as docker container name 
        image: jenkins/inbound_agent    # used docker image
        agent_name: agent_1             # agent name
        port: 8022                      # ssh inbound port
        workDir: /home/agent            # agent workdir
        secret: secret_hash             # agent secret taken from jenkins
    agent_2:
        ...
```
In order to add a new agent, it needs to be created on jenkins first to get agent secret. 
## remote access aka ssh
Role for mass public_key transfer for root user.

### Youtrack
nothing to configure, its strictly to explore YouTrack
