import json
import os
from store.models import DATABASE
from django.contrib.auth import get_user

def filtering_category(database: dict,
                       category_key: [int, str],
                       ordering_key: [None, str] = None,
                       reverse: bool = False):
    """
    Функция фильтрации данных по параметрам

    :param database: База данных.
    :param category_key: [Опционально] Ключ для группировки категории. Если нет ключа, то рассматриваются все товары.
    :param ordering_key: [Опционально] Ключ по которому будет произведена сортировка результата.
    :param reverse: [Опционально] Выбор направления сортировки:
        False - сортировка по возрастанию;
        True - сортировка по убыванию.
    :return: list[dict] список товаров с их характеристиками, попавших под условия фильтрации. Если нет таких элементов,
    то возвращается пустой список
    """
    if category_key is not None:
        result = [value for value in database.values() if category_key == value['category']]  # TODO При помощи фильтрации в list comprehension профильтруйте товары по категории. Или можете использовать
        # обычный цикл или функцию filter
    else:
        result = [value for value in database.values()]  # TODO Трансформируйте database в список словарей
    if ordering_key is not None:
        result.sort(key=lambda x: x[ordering_key], reverse=reverse)  # TODO Проведите сортировку result по ordering_key и параметру reverse
    return result

def view_in_cart(request) -> dict:
    """
    Просматривает содержимое cart.json

    :return: Содержимое 'cart.json'
    """
    if os.path.exists('cart.json'):  # Если файл существует
        with open('cart.json', encoding='utf-8') as f:
            return json.load(f)

    user = get_user(request).username  # Получаем авторизированного пользователя
    cart = {user: {'products': {}}}  # Создаём пустую корзину
    with open('cart.json', mode='x', encoding='utf-8') as f:   # Создаём файл и записываем туда пустую корзину
        json.dump(cart, f)

    return cart

def add_to_cart(request, id_product: str) -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]  # TODO Помните, что у вас есть уже реализация просмотра корзины,
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.

    # TODO Проверьте, а существует ли такой товар в корзине, если нет, то перед тем как его добавить - проверьте есть ли такой
    # id товара в вашей базе данных DATABASE, чтобы уберечь себя от добавления несуществующего товара.
    if id_product in DATABASE and id_product in cart['products']:
        cart['products'][id_product] += 1
    elif id_product in DATABASE and id_product not in cart['products']:
        cart['products'][id_product] = 1
    else:
        return False

    # TODO Если товар существует, то увеличиваем его количество на 1

    # TODO Не забываем записать обновленные данные cart в 'cart.json'
    with open('cart.json', 'w', encoding='utf-8') as f:
        json.dump(cart_users, f)

    return True

def remove_from_cart(request, id_product: str) -> bool:
    """
    Добавляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]  # TODO Помните, что у вас есть уже реализация просмотра корзины,
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.

    # TODO Проверьте, а существует ли такой товар в корзине, если нет, то возвращаем False.
    if id_product not in cart['products']:
        return False
    else:
        cart['products'].pop(id_product)
    with open('cart.json', 'w', encoding='utf-8') as f:
        json.dump(cart_users, f)

    # TODO Если существует товар, то удаляем ключ 'id_product' у cart['products'].

    # TODO Не забываем записать обновленные данные cart в 'cart.json'

    return True

def add_user_to_cart(request, username: str) -> None:
    """
    Добавляет пользователя в базу данных корзины, если его там не было.

    :param username: Имя пользователя
    :return: None
    """
    cart_users = view_in_cart(request)  # Чтение всей базы корзин

    cart = cart_users.get(username)  # Получение корзины конкретного пользователя

    if not cart:  # Если пользователя до настоящего момента не было в корзине, то создаём его и записываем в базу
        with open('cart.json', mode='w', encoding='utf-8') as f:
            cart_users[username] = {'products': {}}
            json.dump(cart_users, f)

def view_in_wishlist(request) -> dict:
    """
    Просматривает содержимое wishlist.json

    :return: Содержимое 'wishlist.json'
    """
    if os.path.exists('wishlist.json'):
        with open('wishlist.json', encoding='utf-8') as f:
            return json.load(f)

    user = get_user(request).username
    wishlist = {user: {'products': []}}
    with open('wishlist.json', mode='x', encoding='utf-8') as f:
        json.dump(wishlist, f)

    return wishlist

def add_to_wishlist(request, id_product: str) -> bool:
    """
    """
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]

    if id_product not in wishlist['products']:
        if not DATABASE.get(id_product):
            return False
        wishlist['products'].append(id_product)
    else:
        return False

    with open('wishlist.json', mode='w', encoding='utf-8') as f:
        json.dump(wishlist_users, f)

    return True

def remove_from_wishlist(request, id_product: str) -> bool:
    """
    """
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]

    if id_product not in wishlist['products']:
        return False
    else:
        wishlist['products'].remove(id_product)

    with open('wishlist.json', mode='w', encoding='utf-8') as f:
        json.dump(wishlist_users, f)

    return True

def add_user_to_wishlist(request, username: str) -> None:
    """
    """
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users.get(username)

    if not wishlist:
        with open('wishlist.json', mode='w', encoding='utf-8') as f:
            wishlist_users[username] = {'products': []}
            json.dump(wishlist_users, f)
