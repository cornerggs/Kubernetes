# Projet de Kubernetes

---

##  Réalisé par

| Nom | numéro d’étudiant | mail |
|-----|-------------|-------------|
| **BENCHEKROUN Soufiane** | 22304603 | soufiane.benchekroun@uphf.fr |
| **LKOUEN Salah Eddine** | 22303080 | salaheddine.lkouen@uphf.fr |

Encadré par : **Mr Hervé Tondeur**

---

## Objectif du projet

L’objectif de cette première étape est de prendre en main l’environnement Kubernetes via Minikube et kubectl, de vérifier son bon fonctionnement et de manipuler les ressources de base (pods, services, images).
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


```


```
