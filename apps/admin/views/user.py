from django.views.generic import ListView, CreateView, UpdateView, DeleteView, RedirectView
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from common.views import LoginRequiredMixin

from accounts.forms import UserForm


User = get_user_model()


class UserListView(LoginRequiredMixin, ListView):

    model = User
    template_name = 'admin/user/list.html'
    context_object_name = 'users'
    paginate_by = settings.PAGE_SIZE


class UserCreateView(LoginRequiredMixin, CreateView):

    model = User
    template_name = 'admin/user/create.html'
    form_class = UserForm

    def get_success_url(self):
        return reverse('admin_user_list')


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    template_name = 'admin/user/edit.html'
    form_class = UserForm
    context_object_name = 'custom_user'

    def get_success_url(self):
        return reverse('admin_user_list')


class UserDeleteView(LoginRequiredMixin, DeleteView):

    model = User
    template_name = 'admin/user/delete.html'

    def get_success_url(self):
        return reverse('admin_user_list')


class UserEnableView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self, pk):
        user = get_object_or_404(User, id=pk)
        user.is_active = True
        user.save()
        return reverse('admin_user_list')


class UserDisableView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self, pk):
        user = get_object_or_404(User, id=pk)
        user.is_active = False
        user.save()
        return reverse('admin_user_list')
