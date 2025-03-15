"""
Пожалуйста, приступайте к этой задаче после того, как вы сделали и получили ревью ко всем остальным задачам
в этом репозитории. Она значительно сложнее.


Есть набор сообщений из чата в следующем формате:

```
messages = [
    {
        "id": "efadb781-9b04-4aad-9afe-e79faef8cffb",
        "sent_at": datetime.datetime(2022, 10, 11, 23, 11, 11, 721),
        "sent_by": 46,  # id пользователя-отправителя
        "reply_for": "7b22ae19-6c58-443e-b138-e22784878581",  # id сообщение, на которое это сообщение является ответом (может быть None)
        "seen_by": [26, 91, 71], # идентификаторы пользователей, которые видели это сообщение
        "text": "А когда ревью будет?",
    }
]
```

Так же есть функция `generate_chat_history`, которая вернёт список из большого количества таких сообщений.
Установите библиотеку lorem, чтобы она работала.

Нужно:
1. Вывести айди пользователя, который написал больше всех сообщений.
2. Вывести айди пользователя, на сообщения которого больше всего отвечали.
3. Вывести айди пользователей, сообщения которых видело больше всего уникальных пользователей.
4. Определить, когда в чате больше всего сообщений: утром (до 12 часов), днём (12-18 часов) или вечером (после 18 часов).
5. Вывести идентификаторы сообщений, который стали началом для самых длинных тредов (цепочек ответов).

Весь код стоит разбить на логические части с помощью функций.
"""
import random
import uuid
import datetime
import lorem


def generate_chat_history():
    messages_amount = random.randint(200, 1000)
    users_ids = list(
        {random.randint(1, 10000) for _ in range(random.randint(5, 20))}
    )
    sent_at = datetime.datetime.now() - datetime.timedelta(days=100)
    messages = []
    for _ in range(messages_amount):
        sent_at += datetime.timedelta(minutes=random.randint(0, 240))
        messages.append({
            "id": uuid.uuid4(),
            "sent_at": sent_at,
            "sent_by": random.choice(users_ids),
            "reply_for": random.choice(
                [
                    None,
                    (
                        random.choice([m["id"] for m in messages])
                        if messages else None
                    ),
                ],
            ),
            "seen_by": random.sample(users_ids,
                                     random.randint(1, len(users_ids))),
            "text": lorem.sentence(),
        })
    return messages


def who_wrote_most(message):
    users_write = {}
    for part in message:
        if part['sent_by'] not in users_write:
            users_write[part['sent_by']] = 1
        else:
            users_write[part['sent_by']] += 1
    result = max(users_write, key=users_write.get)
    count_result = users_write[result]
    return result, count_result


def who_is_most_popular(message):
    users_answer = {}
    for part in message:
        if part['reply_for'] == None:
            continue

        if part['reply_for'] not in users_answer:
            users_answer[part['reply_for']] = 1
        else:
            users_answer[part['reply_for']] += 1
    for part in message:
        if part['id'] == max(users_answer, key=users_answer.get):
            result = part['sent_by']
            count_result = users_answer[max(users_answer, key=users_answer.get)]
    return result, count_result


def who_is_most_visible(message):
    users_seen = {}
    for part in message:
        if part['sent_by'] not in users_seen:
            users_seen[part['sent_by']] = part['seen_by']
        else:
            users_seen[part['sent_by']] + part['seen_by']
    for user, list_users in users_seen.items():
        users_seen[user] = len(set(list_users))
    for top in range(1, 4):
        print(f'{top}. Id пользователя: {max(users_seen, key=users_seen.get)} - {users_seen[max(users_seen, key=users_seen.get)]} ответов!')
        del users_seen[max(users_seen, key=users_seen.get)]


def who_is_most_active_part_of_day(message):
    part_of_day_activity = {
        "Утро": 0,
        "День": 0,
        "Вечер": 0,
        "Ночь": 0,
    }
    for part in message:
        message_hour = part["sent_at"].hour
        if message_hour > 4 and message_hour < 12:
            part_of_day_activity["Утро"] += 1
        elif message_hour >= 12 and message_hour < 18:
            part_of_day_activity["День"] += 1
        elif message_hour >= 18 and message_hour < 24:
            part_of_day_activity["Вечер"] += 1
        else:
            part_of_day_activity["Ночь"] += 1
    result = max(part_of_day_activity, key=part_of_day_activity.get)
    count_result = part_of_day_activity[result]
    return result, count_result


def the_longest_holy_war(message):
    holy_war_length = {}
    for part in message:
        if part["id"] not in holy_war_length:
            holy_war_length[part["id"]] = [part["id"]]
            continue
    for message_id in holy_war_length:
        for part in message:
            if part["reply_for"] == None:                            # Я так и не смог сформулировать для себя что такое "тред" поэтому 2 версии.
                continue                                             # if part["reply_for"] == holy_war_length[message_id][-1]: - последовательная версия
            if part["reply_for"] in holy_war_length[message_id]:     # if part["reply_for"] in holy_war_length[message_id]: - связанная версия
                holy_war_length[message_id].append(part["id"])
    for message_id, tred_message_id in holy_war_length.items():
        holy_war_length[message_id] = len(tred_message_id)
    for top in range(1, 4):
        result = max(holy_war_length, key=holy_war_length.get)
        count_result = holy_war_length[result] - 1
        print(f'{top}. Id сообщения: {result}, длина треда {count_result}!')
        del holy_war_length[result]


def main():
    message = generate_chat_history()
    wrote_most, count_wrote_most = who_wrote_most(message)
    most_answer, count_most_answer = who_is_most_popular(message)
    most_active_part_of_day, count_active_part_of_day = who_is_most_active_part_of_day(message)
    print('1.')
    print(f'Id пользователя, который написал больше всех сообщений:\nId: {wrote_most} - {count_wrote_most} сообщений!')
    print()
    print('2.')
    print(f'Id пользователя, на сообщения которого больше всего отвечали:\nId: {most_answer} - {count_most_answer} ответов!')
    print()
    print('3.')
    print('Id пользователей, сообщения которых видело больше всего уникальных пользователей:')
    who_is_most_visible(message)
    print()
    print('4.')
    print(f'Самая активная часть дня в чате: {most_active_part_of_day} - {count_active_part_of_day} сообщений!')
    print()
    print('5.')
    print('Идентификаторы сообщений, который стали началом для самых длинных тредов:')
    the_longest_holy_war(message)


if __name__ == "__main__":
    main()
