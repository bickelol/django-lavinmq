# Notes pour l'utilisation du projet exploitation


## A- Pré-requis avant le démarrage du projet/ Configuration

### 1- Commande pour installer le projet (prendre le projet depuis github/ gitlab):
```
    git clone https://github.com/<userspace>/<project_name>.git
```

### 2- Configurer les variables d'environnement (locales ou de production)
Que vous fassiez un déploiement local ou en production, il est nécessaire de configurer les variables d'environnement. 
Pour cela, vous pouvez utiliser un fichier `.env` à la racine du projet si c'est local, mais si c'est en production,
utilisez les fichiers dans le dossier `bcorp_django_brokers/config/`.

### 3- Utiliser la commande suivante pour créer un environnement virtuel (à la racine du dossier parent au projet):
```
    uv venv ../<virtual_env_name>
```

### 4- Executer la commande ci-dessous pour passer en environnement virtuel:
```
    source <virtual_env_name>/bin/activate
```

### 5- Utiliser la commande suivante pour installer les dépendances du projet:
```
    uv sync --active 
```

### 6- Exécuter les migrations avec la commande suivante:
```
    uv run --active python3 manage.py migrate 
```



## B- Installation et démarrage du broker lavinmq de docker/podman :

### 1- Installation de l'infrastructure de lavinmq:
Pour installer docker ou podman sur votre machine, vous pouvez utiliser les documentations officielles ou les liens
URL suivants:
- <https://blog.stephane-robert.info/docs/conteneurs/moteurs-conteneurs/docker/installation/>
- <https://podman.io/docs/installation>
- <https://doc.ubuntu-fr.org/docker-compose> pour docker-compose
- <https://www.datacamp.com/fr/tutorial/podman-compose> pour podman-compose

### 2- Installation de l'infrastructure de lavinmq:
Il faut se positionner à la racine du projet dans un terminal et exécuter la commande ci-dessous pour démarrer le broker lavinmq: 
```
    docker-compose -f lavinmq.docker-compose.yml up -d
```
ou 
```
    docker compose -f lavinmq.docker-compose.yml up -d
```
ou
```
    podman-compose -f lavinmq.docker-compose.yml up -d
```
ou
```
    podman compose -f lavinmq.docker-compose.yml up -d
```
NB: Vous devez choisir l'une de ces commandes selon le contexte que vous ayez installé docker ou podman. 
Ensuite, si votre système d'exploitation accepte la commande ```docker-compose``` ou ```podman-compose```.

## C- Démarrage du projet

### 1- Exécuter le projet django avec la commande suivante:
```
    uv run --active python3 manage.py runserver <port>
```

### 2- Exécuter le worker lavinmq avec la commande suivante:
```
    uv run --active python manage.py run_worker   
```