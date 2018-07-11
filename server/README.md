# FreiRaum Server

## Allgemein

FreiRaum ist eine Web Applikation, welche es jedem Studenten an der DHBW Friedrichshafen ermöglicht nach freien Räumen an der DHBW zu suchen. Studenten können sich zudem ihren aktuellen Vorlesungsplan anzeigen lassen.

Die Server stellen dabei einerseits die statischen Dateien und andererseits eine REST-API bereit.

Python 3.6 wird empfohlen, aber alle Funktionalitäten wurden auch mit einem Raspberry Pi der 3. Generation mit aktuellem Raspbian "Stretch" (Python 3.5.3) getestet.

### API

1. "pure_flask": Implementierung des Servers mit Flask
	* Vorteile: Funktionsweise ist einfach zu überschauen, gut erweiterbar
	* Nachteile: Noch kein production ready Server eingebaut 

2. "swagger_flask": aus dem swagger-file generierter Code
	* Vorteile: "gevent" oder "tornado" können einfach als Server davorgeschaltet werden
	* Nachteile: Unübersichtlicher, weitere Dependencies, schlechter Erweiterbar

### Webserver:
Auch hier gibt es wieder zwei Varianten:
Beide Unterstützen den HTML5 push state der vom Frontend benötigt wird.

nginx

python3 webserver

## Requirements
Python 3.4 und neuer

Optional:
- nginx
- Python 3.5.2+ für swagger

## Raspberry Tutorial

Man benötigt general AND (swagger OR pure_flask) AND (simple webserver OR nginx)

### general
```bash
sudo apt update
sudo apt upgrade
sudo apt install git python3-pip
git clone https://github.com/JosefProbst/FreiRaum_DHBW.git
```

### swagger
```bash
cd ~/FreiRaum_DHBW/server/swagger_flask
pip3 install -r requirements.txt # currently fails because connexion depends on pyyaml https://github.com/yaml/pyyaml/issues/201
python3 -m swagger_server &
```

### pure_flask
```bash
cd ~/FreiRaum_DHBW/server/pure_flask
pip3 install -r requirements.txt 
python3 app.py &
```

### simple webserver
```bash
cp ~/FreiRaum_DHBW/server/pure_flask/webserver.py ~/FreiRaum_DHBW/client/dist/freiraum/
cd ~/FreiRaum_DHBW/client/dist/freiraum/
sudo python3 webserver.py &
```
	
### nginx
```bash
sudo apt install nginx
```
Modifiziere den folgenden Block nach deinen Bedürfnissen und füge ihn in den "http Block" von /etc/nginx/nginx.conf ein.

    server {
		listen 80;
		server_name example.org;	# or the ip
		root /home/pi/FreiRaum_DHBW/client/dist/freiraum;	#actually: /path/to/dir/of/index.html
		index index.html
		gzip_static on;
		location / {
			try_files $uri /index.html;
		}
	}
Diese Zeile muss noch gelöscht werden:
	include /etc/nginx/sites-enabled/*;
... genau wie diese Datei
```bash
sudo rm /var/www/html/index.nginx-debian.html
```
Danach sollte nginx neu gestartet werden:
```bash
sudo systemctl restart nginx.service
```
## TODO

- [ ] Kontakt zu den Verantwortlichen in Karlsruhe aufnehmen
- [ ] RAPLA Schnittstellen analysieren und die Beste herausfinden
- [ ] Schnittstelle zu RAPLA implementieren
- [ ] create_random_database() durch die neue Funktion austauschen
- [ ] Werkzeug durch einen production ready server ersetzen
- [ ] Python Webserver: Multithreading, Security
- [ ] Deployment auf freiraum.it.dhbw-ravensburg.de + Touchscreens
- [ ] Weitere Features

## Kontakt
Server:     <josefprobst7@googlemail.com>

	
