# Yookassa-Billing 
https://github.com/netshy/graduate_work
## Yandex Practicum graduate work
##### This project was implemented as a graduation assignment in the middle Python course at Yandex Practicum.
![](https://i.ibb.co/60Pnnbt/image.png)

## Task
Implement the "Billing" project. Two methods for working with cards must be developed: paying for a subscription and refunding the payment. The system should be resilient to interruptions: there should be no double charges, and users should always have the guarantee that the operation has been executed. Besides implementing the system, integrate it with Django's admin panel so you can monitor client subscription payments.

## Layout
![](https://pictures.s3.yandex.net/resources/Diplom_idea_2_1618269965.jpg)


## Features
- Users can pay for a subscription.
- Users can get a refund if they unsubscribe.
- The refund amount is calculated based on the subscription's days since payment.
- Administrators have the functionality to view and manually configure individual subscriptions.
- Email notifications are sent via Mailgun about user transactions (successful/unsuccessful/refund).
- Status checks of transactions in case of network disruptions.

## Architecture
![](https://i.ibb.co/ZgXMtf5/billing-drawio-1.png)

## Get subscription user flow
1. User registers.
2. User logs in and receives an access token.
3. User selects a subscription plan with subscription_plan_id.
4. Yookassa generates a link for subscription payments.
5. User successfully pays.
6. User receives an email confirming the successful payment.
7. Subscription is activated.

## Get refund user flow
1. User specifies the active subscription to cancel with subscription_id.
2. User receives an email confirming the cancellation of the subscription.
3. Subscription is canceled.

## For the convenience of sending requests, a collection is prepared in [Postman](https://github.com/netshy/graduate_work/blob/main/Yookassa%20Billing.postman_collection.json) | [Environments](https://github.com/netshy/graduate_work/blob/main/Billing%20project.postman_environment.json)
