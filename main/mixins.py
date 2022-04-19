from personal.forms import RegisterForm


class FromsMixin:

    def get_register_form(self):
        form = RegisterForm
        return {'register_form': form}
