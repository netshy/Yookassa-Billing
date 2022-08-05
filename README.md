# Yookassa-Billing 
https://github.com/netshy/graduate_work
## Yandex Practicum graduate work
##### Проект реализован в качестве дипломного задания на курсе middle python 
![](https://i.ibb.co/60Pnnbt/image.png)

### Сайт развернут в интернете (только бэк, исключение django)
https://billingpracticum.ru/



## Task
Выполните проект «Биллинг». Нужно сделать два метода работы с картами: оплатить подписку и вернуть за неё деньги. При этом система должна быть устойчивой к перебоям: не должно происходить двойных списаний, и чтобы у пользователя всегда была гарантия, что операция выполнилась. Помимо реализации системы, интегрируйте эту систему с админкой Django, чтобы вы могли контролировать оплату подписок клиентами.

## Layout
![](https://pictures.s3.yandex.net/resources/Diplom_idea_2_1618269965.jpg)


## Features

- Пользователь может оплатить подписку
- Может получить возврат средств, если отпишется
- Сумма возврата расчитывается в зависимости от количества дней использования подписки с момента оплаты
- У администратора есть функциональсть для просмотра и ручной настройки отдельных подписок
- Отправка уведомлений по email через `mailgun` об транзакциях пользователя (Успешных/неуспешных/возврат средств) 
- Проверка статусов транзаций в случае сетевых перебоев

## Architecture
![](https://i.ibb.co/VvzNm3m/billing-arch-drawio.png)

## Get subscription user flow
1. регистрируется
2. логинится и получает `access token`
3. выбирает тарифный план `subscription_plan_id`
4. юкасса генерирует ссылку для оплаты подписки
5. успешно оплачивает
6. получает email об успешности оплаты
7. подписка оформлена!

## Get refund user flow
1. указывает актуальную подписку для отмены `subscription_id
2. получает email об отмене подписки
3. подписка отменена!

## Для удобства отправки запросов подготовленна коллекция в [Postman](https://github.com/netshy/graduate_work/blob/main/Yookassa%20Billing.postman_collection.json) | [Environments](https://github.com/netshy/graduate_work/blob/main/Billing%20project.postman_environment.json)

### Admin panel billing
https://billingpracticum.ru/billing/admin/
login: `n`
password: `1`
