from django.db import models

# Модель Пользователей
class User(models.Model):
    username = models.CharField(max_length=255, verbose_name = "Имя пользователя в Телеграм")
    tg_id = models.IntegerField(verbose_name = "ID пользователя в Телеграм")
    join_datetime = models.DateTimeField(verbose_name = "Дата регистрации", auto_now_add=False)

    def __str__(self):
        return self.username
    
    class Meta:
         verbose_name = "Пользователь"
         verbose_name_plural = "Пользователи"



# Модель Связанных пользователей
class RelatedUser(models.Model):
    first_user = models.ForeignKey(User, verbose_name = "Первый пользователь", on_delete=models.CASCADE, related_name = "first_user", null=True)
    second_user = models.ForeignKey(User, verbose_name = "Второй пользователь", on_delete=models.CASCADE, related_name = "second_user", null=True)
    
    class Meta:
         verbose_name = "Связанный пользователь"
         verbose_name_plural = "Связанные пользователи"


# Модель Чеклистов
class Whishlist(models.Model):
    owner = models.ForeignKey(User, verbose_name = "Автор wish-листа", on_delete=models.CASCADE, related_name = "user_whishlist", null=True)
    creation_date = models.DateTimeField(verbose_name = "Дата создания wish-листа", auto_now_add=False)
    
    class Meta:
         verbose_name = "Whish-лист"
         verbose_name_plural = "Whish-листы"


# Модель Элементов чеклистов
class Whishlist_item(models.Model):
    Whish_list = models.ForeignKey(Whishlist, verbose_name = "ID Whish-листа", on_delete=models.CASCADE, related_name = "Whishlist_item", null=True)
    Whish_list_title = models.CharField(max_length=255, verbose_name = "Заголовок элемента Whish-листа")
    Whish_list_item = models.CharField(max_length=255, verbose_name = "Элемент Whish-листа")
    
    class Meta:
         verbose_name = "Элемент Whish-листа"
         verbose_name_plural = "Элементы Whish-листа"


# Модель уведомлений
class Notification(models.Model):
    notify_text = models.TextField(verbose_name = "Текст уведомления")
    
    class Meta:
         verbose_name = "Уведомление"
         verbose_name_plural = "Уведомления"


# Модель журнала уведомлений
class Notify_journal(models.Model):
    notify_text = models.TextField(verbose_name = "Текст уведомления")
    sent_datetime = models.DateTimeField(verbose_name = "Дата отправки уведомления", auto_now_add=False)
    
    class Meta:
         verbose_name = "Журнал уведомления"
         verbose_name_plural = "Журнал уведомления"


# Модель событий
class UserEvents(models.Model):
    user = models.ForeignKey(User, verbose_name = "Пользователь", on_delete=models.CASCADE, related_name = "Whishlist_item", null=True)
    event_name = models.CharField(max_length=255, verbose_name = "Название события")
    event_date = models.DateTimeField(verbose_name = "Дата события", auto_now_add=False)
    
    class Meta:
         verbose_name = "Событие пользователя"
         verbose_name_plural = "События пользователей"

# Модель настроек
class Settings(models.Model):
    start_message_text = models.TextField(verbose_name = "Текст сообщения для команды /start")
    help_message_text = models.TextField(verbose_name = "Текст сообщения для команды /help")
    notify_interval = models.IntegerField(verbose_name = "Интервал отправки уведомлений (в днях)")
    notify_time = models.IntegerField(verbose_name = "Интервал отправки уведомлений (в днях)")
    user_event_delta = models.IntegerField(verbose_name = "Количество дней до события для уведомления (в днях)")
    
    class Meta:
         verbose_name = "Настройка"
         verbose_name_plural = "Настройки"