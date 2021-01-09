from datetime import datetime, timedelta

class Validations:
    def set_attributes(self, request, **kwargs):
        self.request = request
        self.today = datetime.now()
        self.user = request.data['user']
        self.initial_day = datetime.strptime(request.data['initial_day'], "%Y-%m-%d")
        self.reservation_ends = datetime.strptime(request.data['reservation_ends'], "%Y-%m-%d")

    def initial_day_gte_then_today_validation(self):
        if self.today - timedelta(days=1) > self.initial_day:
            content = {'Error': 'Initial day date must not be earlier than today.'}
            return content

    def Initial_date_gte_end_date_validation(self):
        if self.initial_day > self.reservation_ends:
            content = {'Error': 'Initial day date must not be greater than reservation_ends.'}
            return content

    def two_months_validation(self):
        after_2_months = self.today + timedelta(days=60)

        if after_2_months - self.today < self.initial_day - self.today:
            content = {'Error': "It's very far in time."}
            return content

    def two_weeks_validation(self):
        after_2_weeks = self.initial_day + timedelta(days=14)

        if after_2_weeks - self.initial_day < self.reservation_ends - self.initial_day:
            content = {'Error': 'Maximum 2 weeks.'}
            return content

    def reservation_owner_validation(self):
        content = {'Error': 'Required is your username.'}

        username = self.user

        if self.request.user.username != username and not self.request.user.is_staff:
            return content

    def run_all_validations(self, request, **kwargs):
        self.set_attributes(request, **kwargs)

        validations = [
            self.initial_day_gte_then_today_validation(),
            self.Initial_date_gte_end_date_validation(),
            self.two_months_validation(),
            self.two_weeks_validation(),
            self.reservation_owner_validation(),
        ]
        for validation in validations:
            try:
                if validation:
                    return validation
            except TypeError:
                return False