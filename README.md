# otusapistreamprocessing

# Теория

## HTTP взаимодействие

Преимущества:
* Простота реализации.

Недостатки:
* В момент создания заказа пользователь ожидает ответа от `Notification Service`.
* Ошибки `Notification Service` могут повлиять на стабильность и производительность создания заказа.

```plantuml
@startuml
group Register a user
    User -> "User Service": POST /register/

    activate "User Service"
        "User Service" -> "Billing Service": POST /account/

        activate "Billing Service"
            "Billing Service" --> "User Service": 201 CREATED {account_id}
        deactivate "Billing Service"

        "User Service" -> User: 201 CREATED
    deactivate "User Service"
end

group Charge a user account
    User -> "Billing Service": POST /transaction/

    activate "Billing Service"
        "Billing Service" --> User: 200 OK
    deactivate "Billing Service"
end

group Create an order
    User -> "Order Service": POST /order/
    activate "Order Service"
        "Order Service" -> "Billing Service": POST /transaction/

        activate "Billing Service"
            "Billing Service" --> "Order Service": 200 OK
        deactivate "Billing Service"

        "Order Service" -> "Notification Service": POST /notification/
        activate "Notification Service"
            "Notification Service" -> "Notification Service": Send an email
            "Order Service" --> "Notification Service": 200 OK
        deactivate "Notification Service"

        "Order Service" --> User: 200 OK
    deactivate "Order Service"
end

@enduml
```

## Событийное взаимодействие с использование брокера сообщений для нотификаций (уведомлений)

Преимущества:
* Простота реализации.

Недостатки:
* Избыточные данные в payload сообщений или избыточные запросы `Notification Service` к другим сервисам.

```plantuml
@startuml
group Register a user
    User -> "User Service": POST /register/

    activate "User Service"
        "User Service" -> "Billing Service": POST /account/

        activate "Billing Service"
            "Billing Service" --> "User Service": 201 CREATED {account_id}
        deactivate "Billing Service"

        "User Service" -> User: 201 CREATED
    deactivate "User Service"
end

group Charge a user account
    User -> "Billing Service": POST /transaction/

    activate "Billing Service"
        "Billing Service" --> User: 200 OK
    deactivate "Billing Service"
end

group Create an order
    User -> "Order Service": POST /order/
    activate "Order Service"
        "Order Service" -> "Billing Service": POST /transaction/

        activate "Billing Service"
            "Billing Service" --> "Order Service": 200 OK
        deactivate "Billing Service"

        "Order Service" -> "Message Broker": publish

        "Order Service" --> User: 200 OK
    deactivate "Order Service"

    activate "Message Broker"
        note right
        **OrderConfirmed**

        Contains a detailed information
        about an order.
        end note
        "Message Broker" --> "Notification Service": consume
    deactivate "Message Broker"

    activate "Notification Service"
        "Notification Service" -> "Notification Service": Send an email
    deactivate "Notification Service"
end
@enduml
```

## Event Collaboration cтиль взаимодействия с использованием брокера сообщений

Преимущества:
* Гибкое решение, которое позволит относительно легко вносить изменения в логику работы системы.

Недостатки:
* Сложность реализации и эксплуатации.
* Необходимо поддерживать целостность данных.

```plantuml
@startuml
group Register a user
    User -> Gateway: POST /register/

    activate Gateway
        note right: RegistrationRequested
        Gateway -> "Message Broker": publish
    deactivate Gateway

    activate "Message Broker"
        "Message Broker" --> "User Service": consume
    deactivate "Message Broker"

    activate "User Service"
        "User Service" -> "Message Broker": publish
    deactivate "User Service"

    activate "Message Broker"
        note left: UserCreated
        "Message Broker" --> Gateway: consume
        activate Gateway
            Gateway -> User: 201 CREATED
        deactivate Gateway

        "Message Broker" --> "Notification Service": consume

        activate "Notification Service"
            "Notification Service" -> "Notification Service": Store an email
        deactivate "Notification Service"

        "Message Broker" --> "Billing Service": consume
    deactivate "Message Broker"

    activate "Billing Service"
        "Billing Service" -> "Billing Service": Create an account
        "Billing Service" -> "Message Broker": publish
        note left: AccountCreated
    deactivate "Billing Service"
end

group Charge a user account
    User -> Gateway: POST /transaction/

    activate Gateway
        note right: TransactionRequested
        Gateway -> "Message Broker": publish
    deactivate Gateway

    activate "Message Broker"
        "Message Broker" --> "Billing Service": consume
    deactivate "Message Broker"

    activate "Billing Service"
        "Billing Service" -> "Message Broker": publish
    deactivate "Billing Service"

    activate "Message Broker"
        note left: TransactionCreated
        "Message Broker" --> Gateway: consume
    deactivate "Message Broker"

    activate Gateway
        Gateway -> User: 201 CREATED
    deactivate Gateway
end

group Create an order
    User -> Gateway: POST /order/

    activate Gateway
        note right: OrderRequested
        Gateway -> "Message Broker": publish
    deactivate Gateway

    activate "Message Broker"
        "Message Broker" --> "Order Service": consume
    deactivate "Message Broker"

    activate "Order Service"
        "Order Service" -> "Order Service": Create an order
        "Order Service" -> "Message Broker": publish
    deactivate "Order Service"

    activate "Message Broker"
        note left: OrderCreated
        note left: TransactionRequested
        "Message Broker" --> "Billing Service": consume
    deactivate "Message Broker"

    activate "Billing Service"
        "Billing Service" -> "Billing Service": Debit from the account
        "Billing Service" -> "Message Broker": publish
        note left: TransactionCompleted
    deactivate "Billing Service"

    activate "Message Broker"
        "Message Broker" --> "Order Service": consume
    deactivate "Message Broker"

    activate "Order Service"
        "Order Service" -> "Order Service": Confirm an order
        "Order Service" -> "Message Broker": publish
    deactivate "Order Service"

    activate "Message Broker"
        note left: OrderConfirmed
        "Message Broker" --> Gateway: consume

        activate Gateway
            Gateway -> User: 201 CREATED
        deactivate Gateway

        "Message Broker" --> "Notification Service": consume
    deactivate "Message Broker"

    activate "Notification Service"
        "Notification Service" -> "Notification Service": Send an email
    deactivate "Notification Service"
end
@enduml
```

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
