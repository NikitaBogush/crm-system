from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.list import MultipleObjectMixin

from .forms import LeadForm, TaskForm, DealForm, SalesFunnelForm
from .models import Lead, Task, Deal


@login_required
def index(request):
    """Главная страница. Отображает число задач на сегодня
    и небольшую статистику.
    """
    start_date = date.today() - timedelta(days=7)
    end_date = date.today()
    # Число задач на сегодня (включая просроченные):
    tasks_count = (
        Task.objects.filter(active=True)
        .filter(task_date__lte=date.today())
        .count()
    )
    # Число лидов за последние 7 дней:
    leads_count = Lead.objects.filter(
        date_of_creation__range=(start_date, end_date)
    ).count()
    # Число сделок за последние 7 дней:
    deals_count = Deal.objects.filter(
        date_of_deal__range=(start_date, end_date)
    ).count()
    # Сумма сделок за последние 7 дней:
    deals_sum = Deal.objects.filter(
        date_of_deal__range=(start_date, end_date)
    ).aggregate(Sum("total"))["total__sum"]
    # Если сделок не было:
    if deals_sum is None:
        deals_sum = 0
    template = "leads/index.html"
    context = {
        "tasks_count": tasks_count,
        "leads_count": leads_count,
        "deals_count": deals_count,
        "deals_sum": deals_sum,
    }
    return render(request, template, context)


class LeadsView(LoginRequiredMixin, ListView):
    """Лиды. Выводим по 10 лидов на страницу
    с краткой информацией по каждому.
    """

    model = Lead
    template_name = "leads/leads.html"
    paginate_by = 10


class TasksView(LoginRequiredMixin, ListView):
    """Задачи. Выводим просроченные задачи и
    задачи, запланированные на сегодня.
    """

    model = Task
    template_name = "leads/tasks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Просроченные задачи:
        context["overdue_tasks"] = Task.objects.filter(active=True).filter(
            task_date__lt=date.today()
        )
        # Задачи, запланированные на сегодня:
        context["scheduled_tasks"] = Task.objects.filter(active=True).filter(
            task_date=date.today()
        )
        return context


class DealsView(LoginRequiredMixin, ListView):
    """Сделки. Выводим по 10 сделок на страницу
    с краткой информацией по каждой.
    """

    model = Deal
    template_name = "leads/deals.html"
    paginate_by = 10


@login_required
def sales_funnel(request):
    """Воронка продаж. Выводим статистику продаж за выбранный
    период времени, а также выбирается источник заявок.
    """
    form = SalesFunnelForm(request.GET or None)
    context = {"form": form}
    if form.is_valid():
        # Проверяем корректность выбранного временного интервала:
        if form.cleaned_data["end_date"] < form.cleaned_data["start_date"]:
            form.add_error(
                "end_date",
                "Дата окончания не может быть раньше даты начала",
            )
            return render(request, "leads/sales-funnel.html", context)
        # Дата начала временного интервала:
        start_date = form.cleaned_data["start_date"]
        # Дата окончания временного интервала. Используется в диапазонах,
        # поэтому добавляем плюс один день:
        end_date = form.cleaned_data["end_date"] + timedelta(days=1)
        # Источник заявок:
        source = form.cleaned_data["source"]
        # Если источник не выбран, берем заявки со всех источников:
        if source == "":
            # Количество новых лидов:
            new_leads_count = Lead.objects.filter(
                date_of_creation__range=(start_date, end_date)
            ).count()
            # Новые лиды, совершившие сделку. Статус "2" - это те, кто купил:
            new_leads_with_deals = Lead.objects.filter(
                date_of_creation__range=(start_date, end_date)
            ).filter(status="2")
        # Иначе берем заявки только выбранного источника:
        else:
            new_leads_count = (
                Lead.objects.filter(
                    date_of_creation__range=(start_date, end_date)
                )
                .filter(source=source)
                .count()
            )
            new_leads_with_deals = (
                Lead.objects.filter(
                    date_of_creation__range=(start_date, end_date)
                )
                .filter(source=source)
                .filter(status="2")
            )
        # Количество новых лидов, совершивших сделку:
        new_leads_with_deals_count = new_leads_with_deals.count()
        # Конверсия в сделку, если число новых лидов не равно нулю:
        try:
            conversion = round(
                (new_leads_with_deals_count / new_leads_count) * 100
            )
        # Если число новых лидов равно нулю:
        except ZeroDivisionError:
            conversion = 0
        # Сумма сделок:
        sum = Deal.objects.filter(lead__in=new_leads_with_deals).aggregate(
            Sum("total")
        )["total__sum"]
        # Если сделок не было:
        if sum is None:
            sum = 0
        # Средний чек, если число лидов со сделками не равно нулю:
        try:
            average_bill = round(sum / new_leads_with_deals_count)
        # Если число лидов со сделками равно нулю:
        except ZeroDivisionError:
            average_bill = 0
        context = {
            "new_leads_count": new_leads_count,
            "new_leads_with_deals_count": new_leads_with_deals_count,
            "conversion": conversion,
            "sum": sum,
            "average_bill": average_bill,
            "form": form,
        }
        return render(request, "leads/sales-funnel.html", context)
    return render(request, "leads/sales-funnel.html", context)


class LeadDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    """Информация о лиде. Выводим общую информацию о лиде,
    задачи этого лида (запланированные/просроченные/выполненные),
    сделки, которые заключены с данным лидом.
    """

    model = Lead
    paginate_by = 5  # Паджинация используется для выполненных задач

    def get_context_data(self, **kwargs):
        # Выполненные задачи:
        completed_tasks = (
            Task.objects.filter(lead=self.object)
            .filter(active=False)
            .order_by("-task_date")
        )
        # Добавляем выполненные задачи в object_list для паджинации:
        context = super().get_context_data(
            object_list=completed_tasks, **kwargs
        )
        # Просроченные задачи:
        context["overdue_tasks"] = (
            Task.objects.filter(lead=self.object)
            .filter(active=True)
            .filter(task_date__lt=date.today())
        )
        # Запланированные задачи:
        context["scheduled_tasks"] = (
            Task.objects.filter(lead=self.object)
            .filter(active=True)
            .filter(task_date__gte=date.today())
        )
        # Сделки:
        context["deals"] = Deal.objects.filter(lead=self.object).order_by(
            "-date_of_deal"
        )
        return context


class LeadCreateView(LoginRequiredMixin, CreateView):
    """Создание нового лида."""

    form_class = LeadForm
    template_name = "leads/lead_create.html"

    def form_valid(self, form):
        lead = form.save()
        # При успешном создании лида идет редирект на страницу данного лида:
        return redirect(lead)


class LeadEditView(LoginRequiredMixin, UpdateView):
    """Редактирование информации о лиде."""

    form_class = LeadForm
    model = Lead
    template_name = "leads/lead_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        return context

    def form_valid(self, form):
        lead = form.save()
        return redirect(lead)


class TaskCreateView(LoginRequiredMixin, CreateView):
    """Создание новой задачи для лида."""

    form_class = TaskForm
    template_name = "leads/task_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lead"] = Lead.objects.get(pk=self.kwargs["lead_id"])
        return context

    def form_valid(self, form):
        # Делаем невозможным установить дату задачи в прошлом:
        if form.cleaned_data["task_date"] < date.today():
            form.add_error("task_date", "Нельзя установить дату в прошлом")
            return self.form_invalid(form)
        # Если нажали кнопку "Завершить и создать новую" задачу:
        elif "complete_create_submit" in self.request.POST:
            task = form.save(commit=False)
            task.lead = Lead.objects.get(pk=self.kwargs["lead_id"])
            task.active = False  # Задача больше не активна
            task.save()
            # Редирект на создание новой задачи:
            return redirect("leads:task_create", task.lead.pk)
        # Если нажали кнопку "Завершить" задачу:
        elif "complete_submit" in self.request.POST:
            task = form.save(commit=False)
            task.lead = Lead.objects.get(pk=self.kwargs["lead_id"])
            task.active = False  # задача больше не активна
            task.save()
            # Редирект на страницу лида:
            return redirect("leads:lead_detail", task.lead.pk)
        # Если нажали кнопку "Создать задачу":
        else:
            task = form.save(commit=False)
            task.lead = Lead.objects.get(pk=self.kwargs["lead_id"])
            task.save()
            # Редирект на страницу лида:
            return redirect("leads:lead_detail", task.lead.pk)


class TaskEditView(LoginRequiredMixin, UpdateView):
    """Редактирование задачи для лида."""

    form_class = TaskForm
    model = Task
    template_name = "leads/task_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lead"] = Lead.objects.get(tasks=self.object)
        context["is_edit"] = True
        return context

    def form_valid(self, form):
        # Делаем невозможным установить дату задачи
        # раньше даты создания этой задачи
        if form.cleaned_data["task_date"] < self.object.date_of_creation:
            form.add_error(
                "task_date",
                "Нельзя установить дату задачи раньше даты создания этой задачи",
            )
            return self.form_invalid(form)
        # Если нажали кнопку "Завершить и создать новую" задачу:
        elif "complete_create_submit" in self.request.POST:
            task = form.save(commit=False)
            task.active = False  # Задача больше не активна
            task.save()
            # Редирект на создание новой задачи:
            return redirect("leads:task_create", task.lead.pk)
        # Если нажали кнопку "Завершить" задачу:
        elif "complete_submit" in self.request.POST:
            task = form.save(commit=False)
            task.active = False  # Задача больше не активна
            task.save()
            # Редирект на страницу лида:
            return redirect("leads:lead_detail", task.lead.pk)
        # Если нажали кнопку "Сохранить изменения":
        else:
            task = form.save()
            return redirect("leads:lead_detail", task.lead.pk)


class DealCreateView(LoginRequiredMixin, CreateView):
    """Создание новой сделки для лида."""

    form_class = DealForm
    template_name = "leads/deal_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lead"] = Lead.objects.get(pk=self.kwargs["lead_id"])
        return context

    def form_valid(self, form):
        deal = form.save(commit=False)
        deal.lead = Lead.objects.get(pk=self.kwargs["lead_id"])
        # Меняется статус лида на "2" - купил:
        deal.lead.status = "2"
        # Сохраняем изменения лида:
        deal.lead.save()
        # Сохраняем новую сделку:
        deal.save()
        # Редирект на страницу лида:
        return redirect("leads:lead_detail", deal.lead.pk)


class DealEditView(LoginRequiredMixin, UpdateView):
    """Редактирование сделки для лида."""

    form_class = DealForm
    model = Deal
    template_name = "leads/deal_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lead"] = Lead.objects.get(deals=self.object)
        context["is_edit"] = True
        return context

    def form_valid(self, form):
        deal = form.save()
        # Редирект на страницу лида:
        return redirect("leads:lead_detail", deal.lead.pk)


@login_required
def search(request):
    """Поиск лида по номеру телефона. Если лид с таким номером телефона
    существует, то происходит редирект на его страницу.
    """
    query = request.GET.get("q")
    lead = get_object_or_404(Lead, phone_number__exact=query)
    return redirect("leads:lead_detail", lead.pk)
