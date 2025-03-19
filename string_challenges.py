# Вывести последнюю букву в слове
word = 'Архангельск'
print(word[-1])


# Вывести количество букв "а" в слове
word = 'Архангельск'
print(word.lower().count('а'))


# Вывести количество гласных букв в слове
word = 'Архангельск'
count = 0
for ch in word.lower():
    if ch in {"а", "е", "ё", "и", "о", "у", "ы", "э", "ю", "я"}:
        count += 1
print(count)


# Вывести количество слов в предложении
sentence = 'Мы приехали в гости'
count = len(sentence.split())
print(count)


# Вывести первую букву каждого слова на отдельной строке
sentence = 'Мы приехали в гости'
for word in sentence.split():
    print(word[0])


# Вывести усреднённую длину слова в предложении
sentence = 'Мы приехали в гости'
total = 0
for word in sentence.split():
    total += len(word)
print(total / count)
