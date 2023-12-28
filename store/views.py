from django.http import JsonResponse, HttpResponseNotFound
from django.http import HttpResponse
from django.shortcuts import render
from .models import DATABASE
from logic.services import filtering_category, view_in_cart, add_to_cart, remove_from_cart
# Create your views here.

def product_view(request):
    if request.method == "GET":
        # Обработка id из параметров запроса (уже было реализовано ранее)
        if id_product := request.GET.get("id"):
            if data := DATABASE.get(id_product):
                return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                             'indent': 4})
            return HttpResponseNotFound("Данного продукта нет в базе данных")

        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")  # Считали 'category'
        ordering_key = request.GET.get("ordering")
        if ordering_key: # Если в параметрах есть 'ordering'
            if request.GET.get("reverse") in ('true', 'True', 'TRUE'): # Если в параметрах есть 'ordering' и 'reverse'=True
                data = filtering_category(DATABASE, category_key, ordering_key, True) #  TODO Провести фильтрацию с параметрами
            else:
                data = filtering_category(DATABASE, category_key, ordering_key) #  TODO Провести фильтрацию с параметрами
        else:
            data = filtering_category(DATABASE, category_key) #  TODO Провести фильтрацию с параметрами
        # В этот раз добавляем параметр safe=False, для корректного отображения списка в JSON
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                    'indent': 4}, safe=False)

def show_view(request):
    if request.method == 'GET':
        # with open('store/shop.html', 'r', encoding='utf-8') as f:
        #     data = f.read()
        # return HttpResponse(data)
        return render(request,
                      'store/shop.html',
                      context={"products": DATABASE.values()})


# def products_page_view(request, page):
#     if request.method == "GET":
#         if isinstance(page, str):
#             for data in DATABASE.values():
#                 if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла
#             # TODO 1. Откройте файл open(f'store/products/{page}.html', encoding="utf-8") (Не забываем про контекстный менеджер with)
#             # TODO 2. Прочитайте его содержимое
#             # TODO 3. Верните HttpResponse c содержимым html файла
#                     with open(f'store/products/{page}.html', 'r', encoding='utf-8') as f:
#                         data = f.read()
#                     return HttpResponse(data)
#         elif isinstance(page, int):
#             if str(page) in DATABASE:
#                 with open(f'store/products/{DATABASE[str(page)]["html"]}.html', 'r', encoding='utf-8') as f:
#                     data = f.read()
#                 return HttpResponse(data)
#         # Если за всё время поиска не было совпадений, то значит по данному имени нет соответствующей
#         # страницы товара и можно вернуть ответ с ошибкой HttpResponse(status=404)
#         return HttpResponse(status=404)

def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:
                    return render(request, "store/product.html", context={"product": data})

        elif isinstance(page, int):
            # Обрабатываем условие того, что пытаемся получить страницу товара по его id
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:
                return render(request, "store/product.html", context={"product": data})

        return HttpResponse(status=404)

def cart_view(request):
    if request.method == "GET":
        data = view_in_cart() # TODO Вызвать ответственную за это действие функцию
        if request.GET.get('format') == 'JSON':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
        products = []  # Список продуктов
        for product_id, quantity in data['products'].items():
            # 1. Получите информацию о продукте из DATABASE по его product_id. product будет словарём
            product = DATABASE.get(product_id, {})
            # 2. в словарь product под ключом "quantity" запишите текущее значение товара в корзине
            product["quantity"] = quantity
            # 3. добавьте product в список products
            products.append(product)
            product["price_total"] = f"{quantity * product['price_after']:.2f}"  # добавление общей цены позиции с ограничением в 2 знака

        return render(request, "store/cart.html", context={"products": products})


def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product) # TODO Вызвать ответственную за это действие функцию
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False, 'indent': 4})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product) # TODO Вызвать ответственную за это действие функцию
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False, 'indent': 4})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def shop_view(request):
    if request.method == "GET":
        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
            if request.GET.get("reverse") in ('true', 'True'):
                data = filtering_category(DATABASE, category_key, ordering_key,
                                          True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return render(request, 'store/shop.html',
                      context={"products": data,
                               "category": category_key})