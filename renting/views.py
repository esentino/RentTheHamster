from django.shortcuts import render

from django.views import View

from renting.models import Sala


class AddSalaView(View):
    def get(self, request):
        return render(request, "add_sala.html")

    def post(self, request):
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        has_projector = request.POST.get("has_projector")
        ctx = {}

        if name and capacity:
            # projector = True if has_projector == 'on' else False
            # projector = has_projector == 'on'
            projector = False
            if has_projector == 'on':
                projector = True

            Sala.objects.create(
                name=name, capacity=capacity, has_projector=projector
            )
            ctx['success'] = 'Dodano sale'
        return render(request, 'add_sala.html', ctx)


class ModifySalaView(View):
    def get(self, request, id):
        sala = Sala.objects.get(id=id)
        ctx = {'sala': sala}
        return render(request, 'modify_sala.html', ctx)

    def post(self, request, id):
        sala = Sala.objects.get(id=id)
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        has_projector = request.POST.get("has_projector")
        ctx = {}
        if name and capacity:
            projector = False
            if has_projector == 'on':
                projector = True
            sala.name = name
            sala.capacity = capacity
            sala.has_projector = projector
            sala.save()
            ctx['success'] = 'Zapisano sale'
        ctx['sala'] = sala
        return render(request, 'modify_sala.html', ctx)


class MainView(View):
    def get(self, request):
        salas = Sala.objects.all()
        ctx = {'salas': salas}
        return render(request, 'main.html', ctx)

class SearchView(View):
    def get(self, request):
        name = request.GET.get("name")
        capacity_from = request.GET.get("capacity_from")
        capacity_to = request.GET.get("capacity_to")
        has_projector = request.GET.get("has_projector")

        salas = Sala.objects.all()
        if name:
            salas = salas.filter(name__icontains=name)
        if capacity_from:
            salas = salas.filter(capacity__gte=capacity_from)
        if capacity_to:
            salas = salas.filter(capacity__lte=capacity_to)
        # ma projektor lub ma pojemność większą niż 10
        # from django.db.models import Q
        # salas.filter(Q(has_projector=True) | Q(capacity__gt=10)
        # ma projektor i ma pojemność większą niż 10
        # salas.filter(Q(has_projector=True) & Q(capacity__gt=10)
        # dobra_sala = Q(has_projector=True) & Q(capacity__gt=10)
        # salas.filter(dobra_sala)
        # promocja_na_mala_sale_bez_projektora = Q(has_projector=False) & Q(capacity__lt=6)
        # salas.filter(promocja_na_mala_sale_bez_projektora)

        if has_projector:
            salas = salas.filter(has_projector=True)
        ctx = {'salas': salas}

        return render(request, 'search.html', ctx)
