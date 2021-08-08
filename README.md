# otusapistreamprocessing

# Теория

## HTTP взаимодействие

[Описание REST интерфейсов](http://petstore.swagger.io/?url=https%3A%2F%2Fraw.githubusercontent.com%2Fadalekin%2Fotusstreamprocessing%2Fmaster%2Fdoc%2Fhttp-communication%2Frest-openapi.yaml)

Преимущества:
* Простота реализации.

Недостатки:
* В момент создания заказа пользователь ожидает ответа от `Notification Service`.
* Ошибки `Notification Service` могут повлиять на стабильность и производительность создания заказа.

<img src="./doc/http-communication/sequence-diagram.svg" width="100%">

## Событийное взаимодействие с использование брокера сообщений для нотификаций (уведомлений)

Преимущества:
* Простота реализации.

Недостатки:
* Избыточные данные в payload сообщений или избыточные запросы `Notification Service` к другим сервисам.

<img src="./doc/mb-notifications/sequence-diagram.svg" width="100%">

## Event Collaboration cтиль взаимодействия с использованием брокера сообщений

Преимущества:
* Гибкое решение, которое позволит относительно легко вносить изменения в логику работы системы.

Недостатки:
* Сложность реализации и эксплуатации.
* Необходимо поддерживать целостность данных.

<img src="./doc/event-collaboration/sequence-diagram.svg" width="100%">

# Prerequisites

* Kubernetes 1.21.2
* Helm 3.6.3
* Istio 1.10.3
* Skaffold

# Run

## Add Helm repos

```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add kiali https://kiali.org/helm-charts
helm repo add jaeger https://jaegertracing.github.io/helm-charts
helm repo add prometheus https://prometheus-community.github.io/helm-charts
```

## Run with Skaffold

```
skaffold run
```

# Tests

```
newman run users-auth.postman_collection.json
```
