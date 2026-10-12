# DVWA setup notes (Ubuntu Server agent)

These are the steps used to stand up [DVWA](https://github.com/digininja/DVWA) as the
vulnerable web target on the Linux agent. DVWA is **intentionally vulnerable** — run it only
on an isolated lab network.

> Replace `<AGENT_IP>` with the agent's address and choose your own DB password in place of
> `<DVWA_DB_PASSWORD>`. Do not commit real credentials.

## 1. Install the web stack

```bash
sudo apt-get update
sudo apt-get install -y apache2 mariadb-server php libapache2-mod-php php-mysqli php-gd git
sudo systemctl enable --now apache2 mariadb
```

Sanity check: browse to `http://<AGENT_IP>/` and confirm the Apache default page loads.

## 2. Download DVWA

```bash
sudo git clone https://github.com/digininja/DVWA.git /var/www/html/dvwa
sudo chown -R www-data:www-data /var/www/html/dvwa
sudo chmod -R 755 /var/www/html/dvwa
```

## 3. Create the database

```bash
sudo mysql
```
```sql
CREATE DATABASE dvwa;
CREATE USER 'dvwa'@'localhost' IDENTIFIED BY '<DVWA_DB_PASSWORD>';
GRANT ALL PRIVILEGES ON dvwa.* TO 'dvwa'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## 4. Configure DVWA

```bash
sudo cp /var/www/html/dvwa/config/config.inc.php.dist /var/www/html/dvwa/config/config.inc.php
```
Edit `config.inc.php` so `db_user`, `db_password`, and `db_database` match the database you
just created.

Then enable two PHP settings DVWA needs (adjust the PHP version in the path to match yours —
find it with `php -v`):
```bash
sudo nano /etc/php/<PHP_VERSION>/apache2/php.ini
# set:
#   allow_url_fopen = On
#   allow_url_include = On
sudo systemctl restart apache2
```

## 5. Finish in the browser

Go to `http://<AGENT_IP>/dvwa/setup.php` and click **Create / Reset Database**, then log in
with the DVWA default credentials and set **DVWA Security → Low** so the vulnerabilities are
exercisable.

## 6. Make the web logs visible to Wazuh

Add the Apache access log to the agent config — see
[`agent-ossec.conf.example`](agent-ossec.conf.example) — then restart the agent.

## Safety

- Keep this VM on an **isolated** VMware network.
- **Snapshot the VM** after setup so you can reset to a clean state between attacks.
