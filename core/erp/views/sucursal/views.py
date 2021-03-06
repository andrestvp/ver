from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import SucursalForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Sucursal


class SucursalListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Sucursal
    template_name = 'sucursal/list.html'
    permission_required = 'view_sucursal'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in Sucursal.objects.all():
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Sucursal'
        context['create_url'] = reverse_lazy('erp:sucursal_create')
        context['list_url'] = reverse_lazy('erp:sucursal_list')
        context['entity'] = 'Sucursales'
        return context


class SucursalCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'sucursal/create.html'
    success_url = reverse_lazy('erp:sucursal_list')
    permission_required = 'add_sucursal'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opci??n'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creaci??n una Sucursal'
        context['entity'] = 'Sucursales'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class SucursalUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'sucursal/create.html'
    success_url = reverse_lazy('erp:sucursal_list')
    permission_required = 'change_sucursal'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opci??n'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edici??n una Sucursal'
        context['entity'] = 'Sucursales'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class SucursalDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Sucursal
    template_name = 'sucursal/delete.html'
    success_url = reverse_lazy('erp:sucursal_list')
    permission_required = 'delete_sucursal'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminaci??n de una Sucursal'
        context['entity'] = 'Sucursales'
        context['list_url'] = self.success_url
        return context
