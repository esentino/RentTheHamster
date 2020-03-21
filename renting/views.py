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
        ctx = {'sala': sala}
        if name and capacity:
            projector = False
            if has_projector == 'on':
                projector = True
            sala.name = name
            sala.capacity = capacity
            sala.has_projector = projector
            sala.save()
            ctx['success'] = 'Zapisano sale'
        return render(request, 'modify_sala.html', ctx)
