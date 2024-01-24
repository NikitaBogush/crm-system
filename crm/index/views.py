from django.shortcuts import render

# Create your views here.


def index(request):
    # Адрес шаблона сохраним в переменную, это не обязательно, но удобно
    template = "ice_cream/index.html"
    # Строку, которую надо вывести на страницу, тоже сохраним в переменную
    title = "Анфиса для друзей"
    # Словарь с данными принято называть context
    context = {
        # В словарь можно передать переменную
        "title": title,
        # А можно сразу записать значение в словарь. Но обычно так не делают
        "text": "Главная страница",
    }
    # Третьим параметром передаём словарь context
    return render(request, template, context)
