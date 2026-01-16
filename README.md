# Projet de Messagerie Kafka

---

##  Réalisé par

| Nom | numéro d’étudiant | mail |
|-----|-------------|-------------|
| **BENCHEKROUN Soufiane** | 22304603 | soufiane.benchekroun@uphf.fr |
| **LKOUEN Salah Eddine** | 22303080 | salaheddine.lkouen@uphf.fr |

Encadré par : **Mr Hervé Tondeur**

---

## Objectif du projet

Créer un système de messagerie distribuée basé sur Kafka où :
- Des clients s’enregistrent et échangent des messages
- Chaque message est automatiquement traduit en français
- Les connexions et tous les messages sont archivés dans PostgreSQL
- L’interaction se fait via un client en ligne de commande interactif

---

## Technologies utilisées

<p align="center">
  <img src="https://www.vectorlogo.zone/logos/java/java-icon.svg" alt="Java" width="50"/>
  <img src="https://www.vectorlogo.zone/logos/springio/springio-icon.svg" alt="Spring" width="50"/>
  <img src="https://www.vectorlogo.zone/logos/apache_kafka/apache_kafka-icon.svg" alt="Kafka" width="50"/>
  <img src="https://www.vectorlogo.zone/logos/postgresql/postgresql-icon.svg" alt="PostgreSQL" width="50"/>
  <img src="https://www.vectorlogo.zone/logos/docker/docker-icon.svg" alt="Docker" width="50"/>
</p>

---

## Lancement rapide

### 1. Démarrer tous les services

```bash
cd scripts
sudo ./run_services.sh
```
Cela lance automatiquement :

- Kafka + Zookeeper

- LibreTranslate (API HTTP)

- PostgreSQL

- srv-translate (microservice Spring Boot de traduction)

- client-cons-db (microservice Spring Boot pour l’archivage)

### 2. Lancer les clients CLI
```bash
sudo ./5a_run_cliA.sh
sudo ./5b_run_cliB.sh
```
### 3. Commandes disponibles

```bash
enregistrer-client
message --dst ClientB --msg "hello"
lister-clients
traduire "how are you"
is-connected --client ClientB
byebye
```

### 4. Arrêt propre
```bash
cd scripts
./stop_services.sh
```

## Schéma d’architecture

Voici le schéma global de l’architecture de notre projet de messagerie Kafka avec traduction automatique et archivage :

<p align="center">
  <img src="docs/schema-architecture.png" alt="Schéma d’architecture du projet" width="700"/>
</p>

### Description du fonctionnement

- **Clients A, B, C, D** : chacun peut envoyer et recevoir des messages.  
  Ils utilisent :
  - `topicout` pour **envoyer** un message
  - `topicin` pour **recevoir** une réponse traduite
  - `topictechout` pour **envoyer des commandes** (CONNECT, GET, ISCONNECTED…)
  - `topictechin` pour **recevoir des réponses techniques**

- **Kafka** : le cœur de communication du système, utilisé comme bus de messages entre les services.

- **srv-translate** :
  - Consomme les messages du `topicout`
  - Appelle l’API **LibreTranslate**
  - Publie la traduction dans `topicin`

- **LibreTranslate** : service de traduction HTTP local (en anglais vers français)

- **client-cons-db** :
  - Archive les messages depuis `topicout` et `topicin`
  - Gère les commandes techniques depuis `topictechout`
  - Publie les réponses dans `topictechin`
  - Stocke les informations dans la base **PostgreSQL**

- **PostgreSQL** : base de données contenant deux tables principales :
  - `message` : messages envoyés et traduits
  - `client_connecte` : clients actifs


##  Demo vidéo

Voici une démonstration complète du fonctionnement de notre projet de messagerie Kafka, incluant le lancement des services, les interactions entre clients, la traduction automatique, et l’archivage dans PostgreSQL :

 [Cliquez ici pour voir la démo sur YouTube](https://www.youtube.com/watch?v=PGfgsOkM-AA&t=27s)

# Kubernetes
# Kubernetes
# Kubernetes
# Kubernetes

## Kubernetes / Minikube — Application Étudiants (EDA)

### Prérequis

```bash
minikube start
kubectl cluster-info
```

### Build des images (dans l’environnement Docker de Minikube)

```bash
eval "$(minikube -p minikube docker-env)"

docker build -t backend:1.0 ./backend
docker build -t integration:1.0 ./integration
docker build -t web-backend:1.0 ./web-backend
docker build -t frontend:1.0 ./frontend
```

### Déploiement Kubernetes

```bash
kubectl apply -f k8s/etudiants-namespace.yaml

kubectl apply -f k8s/etudiants-postgres.yaml
kubectl apply -f k8s/etudiants-zookeeper.yaml
kubectl apply -f k8s/etudiants-kafka.yaml

kubectl apply -f k8s/etudiants-backend.yaml
kubectl apply -f k8s/etudiants-integration.yaml
kubectl apply -f k8s/etudiants-web-backend.yaml
kubectl apply -f k8s/etudiants-frontend.yaml
```

Vérifier l’état:

```bash
kubectl -n etudiants get pods -o wide
kubectl -n etudiants get svc -o wide
```

### Accès au frontend

```bash
MINIKUBE_IP=$(minikube ip)
echo "http://${MINIKUBE_IP}:30080"
```

### Tests E2E rapides (sans navigateur)

POST (envoi vers Kafka via backend):

```bash
MINIKUBE_IP=$(minikube ip)
curl -i -X POST "http://${MINIKUBE_IP}:30080/api/etudiants" \
  -H "Content-Type: application/json" \
  -d '{"nom":"Dupont","prenom":"Alice"}'
```

GET (lecture depuis Postgres via web-backend):

```bash
MINIKUBE_IP=$(minikube ip)
curl -sS "http://${MINIKUBE_IP}:30080/db/etudiants" | jq .
```

### Debug (si quelque chose ne démarre pas)

```bash
kubectl -n etudiants describe pod <pod>
kubectl -n etudiants logs deployment/kafka --tail=200
kubectl -n etudiants logs deployment/zookeeper --tail=200
kubectl -n etudiants logs deployment/backend --tail=200
kubectl -n etudiants logs deployment/integration --tail=200
kubectl -n etudiants logs deployment/web-backend --tail=200
kubectl -n etudiants logs deployment/frontend --tail=200
```

Test réseau depuis `shellclient`:

```bash
kubectl -n etudiants exec deployment/shellclient -- sh -lc 'nc -vz -w 2 kafka 9092; nc -vz -w 2 zookeeper 2181; nc -vz -w 2 postgres 5432'
```
