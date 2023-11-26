from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    
    # Перевизначення методу [ready] конфігурації застосунку <users> для виконання завдання ініціалізації,
    # яка реєструє сигнали.
    def ready(self):
        import users.signals