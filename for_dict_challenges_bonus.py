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
from collections import defaultdict


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


def who_wrote_most(messages):
    users_write = defaultdict(int)
    for part in messages:
        users_write[part['sent_by']] += 1
    result = max(users_write, key=users_write.get)
    count_result = users_write[result]
    return result, count_result


def who_is_most_popular(messages):
    users_answer = defaultdict(int)
    for part in messages:
        if part['reply_for'] is None:
            continue
        users_answer[part['reply_for']] += 1
    most_popular_user = max(users_answer, key=users_answer.get)
    for part in messages:
        if part['id'] == most_popular_user:
            result = part['sent_by']
            count_result = users_answer[most_popular_user]
    return result, count_result


def who_is_most_visible(messages):
    users_seen = {}
    for part in messages:
        if part['sent_by'] not in users_seen:
            users_seen[part['sent_by']] = part['seen_by']
        else:
            users_seen[part['sent_by']] + part['seen_by'] # если вставить сделать += - резульаты у всех становсятся одинаковыми
    for user, list_users in users_seen.items():
        users_seen[user] = len(set(list_users))
    for top in range(1, 4):
        max_user = max(users_seen, key=users_seen.get)
        print(f'{top}. Id пользователя: {max_user} - {users_seen[max_user]} ответов!')
        del users_seen[max(users_seen, key=users_seen.get)]


def get_part_of_day(hour):
    if 5 <= hour < 12:
        return "Утро"
    elif 12 <= hour < 18:
        return "День"
    elif 18 <= hour < 24:
        return "Вечер"
    else:
        return "Ночь"


def who_is_most_active_part_of_day(message):
    part_of_day_activity = {
        "Утро": 0,
        "День": 0,
        "Вечер": 0,
        "Ночь": 0,
    }
    for part in message:
        message_hour = part["sent_at"].hour
        part_of_day = get_part_of_day(message_hour)
        part_of_day_activity[part_of_day] += 1  
    result = max(part_of_day_activity, key=part_of_day_activity.get)
    count_result = part_of_day_activity[result]
    return result, count_result


def add_to_thread(part, holy_war_length, message_id, thread_type):
    if thread_type and part["reply_for"] == holy_war_length[message_id][-1]:  # Если True, последовательная версия
        holy_war_length[message_id].append(part["id"])
    elif not thread_type and part["reply_for"] in holy_war_length[message_id]:  # Если False, связанная версия
        holy_war_length[message_id].append(part["id"])


def the_longest_holy_war(messages, thread_type: bool):
    holy_war_length = {}
    for part in messages:
        if part["id"] not in holy_war_length:
            holy_war_length[part["id"]] = [part["id"]]

    for message_id in holy_war_length:
        for part in messages:
            if part["reply_for"] is None:
                continue

            add_to_thread(part, holy_war_length, message_id, thread_type)
    for message_id, tred_message_id in holy_war_length.items():
        holy_war_length[message_id] = len(tred_message_id)
    for top in range(1, 4):
        result = max(holy_war_length, key=holy_war_length.get)
        count_result = holy_war_length[result] - 1
        print(f'{top}. Id сообщения: {result}, длина треда {count_result}!')
        del holy_war_length[result]


def main():
    messages = generate_chat_history()
    wrote_most, count_wrote_most = who_wrote_most(messages)
    most_answer, count_most_answer = who_is_most_popular(messages)
    most_active_part_of_day, count_active_part_of_day = who_is_most_active_part_of_day(messages)
    print('1.')
    print(f'Id пользователя, который написал больше всех сообщений:\nId: {wrote_most} - {count_wrote_most} сообщений!')
    print()
    print('2.')
    print(f'Id пользователя, на сообщения которого больше всего отвечали:\nId: {most_answer} - {count_most_answer} ответов!')
    print()
    print('3.')
    print('Id пользователей, сообщения которых видело больше всего уникальных пользователей:')
    who_is_most_visible(messages)
    print()
    print('4.')
    print(f'Самая активная часть дня в чате: {most_active_part_of_day} - {count_active_part_of_day} сообщений!')
    print()
    print('5.')
    print('Идентификаторы сообщений, который стали началом для самых длинных тредов:')
    print('Последовательная версия')
    the_longest_holy_war(messages, True)
    print('Cвязанная версия')
    the_longest_holy_war(messages, False)


if __name__ == "__main__":
    main()
