from django.contrib.auth.models import User

from gift_card.models import Card


def get_nominal(num):
    index = 0
    if num[:2] == "39":
        index = 2
    if num[index] in "123456":
        if num[index] == "5":
            return 500
        if num[index] == "6":
            return 5000
        return int(num[index] + "000")


def not_valid_number(number):
    if number[-1] == " ":
        return "Уберите пробел в конце номера"
    if not number.isdigit():
        return "Номер не должен содержать буквы или пробелы."
    if len(number) not in (8, 13):
        return "Номер должен содержать 8 или 13 символов."
    index = 0
    if number[:2] == "39":
        index = 2
    if number[index] in "123456":
        return False
    return "Номер карты не соответствует шаблону"


def process_txt_file(file, user):
    count = {"count_edit": 0, "count_new": 0}
    # user = User.objects.get(username="")
    for line in file:
        number = line.decode('utf-8').strip()
        new_card = Card.objects.filter(number=number).first()
        if new_card:
            new_card.user = user
            new_card.save()
            count["count_edit"] += 1
        else:
            new_card = Card()
            new_card.user = user
            new_card.number = number
            new_card.nominal = get_nominal(number)
            new_card.save()
            count["count_new"] += 1

    return count

