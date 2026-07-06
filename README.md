# Odoo Setup

This project runs **Odoo 19** with custom DVZO modules and selected OCA addons.

For upgrading an existing Odoo 16 database, see [MIGRATION.md](MIGRATION.md).

```bash
cp ./config/odoo.conf.example ./config/odoo.conf
# adapt the actual configuration

cp ./docker-compose.env.example ./docker-compose.env
# adapt the actual env variables

docker-compose up -d
```

## Initial Setup

```bash
# install docker
# https://docs.docker.com/engine/install/ubuntu/

# create new user
adduser dvzo
usermod -aG sudo dvzo
usermod -aG docker dvzo
cp -a /root/.ssh /home/dvzo/
chown -R dvzo:dvzo /home/dvzo/.ssh

# set this in /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
systemctl restart sshd

# install caddy
https://caddyserver.com/docs/install

# Apply Caddyfile
caddy reload Caddyfile
```
