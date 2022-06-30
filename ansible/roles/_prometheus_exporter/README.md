# Role paramétré `_prometheus_exporter`

Role paramétré réutilisable pour le déploiement d'exporter Prometheus depuis github

## Paramètres
 - `_prometheus_exporter_name` : nom de l'exporter (ie nom du binaire, du service...) [STRING]
 - `_prometheus_exporter_version` : numero de version (release github) [STRING]
 - `_prometheus_exporter_github` : projet github sous la forme 'profile/projet'  [STRING]
 - `_prometheus_exporter_sha256` : checksum sha256 du tarball de la release téléchargé depuis github [STRING]
 - `_prometheus_exporter_port`: port utilisé par l'exporter (normalement >= 9100) [INTEGER]
 - `_prometheus_exporter_args`: arguments en ligne de commande à ajouter dans le service systemd [STRING]
 - `_prometheus_exporter_env`: variables d'environement à ajouter dans le service systemd [ARRAY]
 - `_prometheus_exporter_server`: nom du serveur prometheus pour alimenter le fichier de découverte auto des targets (`file_sd_configs`)
 - `_prometheus_exporter_job`: nom du job prometheus pour nommer le fichier de découverte auto des targets (ex: `targets/node.yml` )
 

## Utilisation

Il faut charger dynamiquement le role :

```
- include_role:
    name: _prometheus_exporter
  vars:
    _prometheus_exporter_name: node_exporter
    _prometheus_exporter_version:  0.18.1
    _prometheus_exporter_github: prometheus/node_exporter
    _prometheus_exporter_sha256: b2503fd932f85f4e5baf161268854bf5d22001869b84f00fd2d1f57b51b72424
    _prometheus_exporter_port: 9100
    _prometheus_exporter_args: "--collector.systemd"
    _prometheus_exporter_server: oscaradmin01 
    _prometheus_exporter_job: node

```
