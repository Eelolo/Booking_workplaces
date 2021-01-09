from datetime import datetime, timedelta

class Validations:
    def set_attributes(self, request, **kwargs):
        self.request = request
        self.today = datetime.now()
        self.initial_day = datetime.strptime(request.data['initial_day'], "%Y-%m-%d")

    def initial_day_gte_then_today_validation(self):
        if self.today - timedelta(days=1) > self.initial_day:
            content = {'Error': 'Initial day date must not be earlier than today.'}
            return content

    def run_all_validations(self, request, **kwargs):
        self.set_attributes(request, **kwargs)

        validations = [
            self.initial_day_gte_then_today_validation(),

        ]
        for validation in validations:
            try:
                if validation:
                    return validation
            except TypeError:
                return False