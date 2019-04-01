from django.views.generic import UpdateView
from lock_tokens.exceptions import AlreadyLockedError
from lock_tokens.sessions import check_for_session, lock_for_session, unlock_for_session
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


class LockableUpdateView(UpdateView):
    default_lock_message = "Impossible d'acceder à la page : l'objet est en cours de modification."
    default_success_message = "Les modifications ont bien été enregistrées."
    default_context = {}

    def lock(self, request):
        try:
            lock_for_session(self.get_object(), request.session)
            return True
        except AlreadyLockedError:
            messages.error(request, getattr(self, 'lock_message', self.default_lock_message))
            return False

    def get(self, request, *args, **kwargs):
        if not self.lock(request):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.lock(request):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if not check_for_session(self.get_object(), self.request.session):
            messages.error(request, getattr(self, 'lock_message', self.default_lock_message))
            return redirect(request.META.get('HTTP_REFERER', '/'))
        messages.success(self.request, getattr(self, 'success_message', self.default_success_message))
        self.object = form.save()
        unlock_for_session(self.get_object(), self.request.session)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, **getattr(self, 'context', self.default_context)}
