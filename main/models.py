from django.db import models

# Модель Пользователей
class Users(models.Model):
    username = models.CharField(max_length=255, verbose_name = "Имя пользователя в Телеграм")
    tg_id = models.IntegerField(verbose_name = "ID пользователя в Телеграм")
    join_datetime = models.DateTimeField(verbose_name = "Дата регистрации", auto_now_add=False)

    def __str__(self):
        return self.username
    
    class Meta:
         verbose_name = "Пользователь"
         verbose_name_plural = "Пользователи"



# # Модель Связанных пользователей
# class RelatedUser(models.Model):
#     first_user = models.ForeignKey(User, verbose_name = "Первый пользователь", on_delete=models.CASCADE, related_name = "first_user", null=True)
#     second_user = models.ForeignKey(User, verbose_name = "Второй пользователь", on_delete=models.CASCADE, related_name = "second_user", null=True)
    
#     class Meta:
#          verbose_name = "Связанный пользователь"
#          verbose_name_plural = "Связанные пользователи"


# Модель Вишлистов
class Whishlist(models.Model):
    owner = models.ForeignKey(Users, verbose_name = "Автор wish-листа", on_delete=models.CASCADE, related_name = "user_whishlist", null=True)
    creation_date = models.DateTimeField(verbose_name = "Дата создания wish-листа", auto_now_add=False)
    
    class Meta:
         verbose_name = "Whish-лист"
         verbose_name_plural = "Whish-листы"


# Модель Элементов вишлистов
class Whishlist_item(models.Model):
    Whish_list = models.ForeignKey(Whishlist, verbose_name = "ID Whish-листа", on_delete=models.CASCADE, related_name = "Whishlist_item", null=True)
    Whish_list_title = models.CharField(max_length=255, verbose_name = "Заголовок элемента Whish-листа")
    Whish_list_item = models.CharField(max_length=255, verbose_name = "Элемент Whish-листа")
    
    class Meta:
         verbose_name = "Элемент Whish-листа"
         verbose_name_plural = "Элементы Whish-листа"


# # Модель уведомлений
# class Notification(models.Model):
#     notify_text = models.TextField(verbose_name = "Текст уведомления")
    
#     class Meta:
#          verbose_name = "Уведомление"
#          verbose_name_plural = "Уведомления"


# # Модель журнала уведомлений
# class Notify_journal(models.Model):
#     notify_text = models.TextField(verbose_name = "Текст уведомления")
#     sent_datetime = models.DateTimeField(verbose_name = "Дата отправки уведомления", auto_now_add=False)
    
#     class Meta:
#          verbose_name = "Журнал уведомления"
#          verbose_name_plural = "Журнал уведомления"


# # Модель событий
# class UserEvents(models.Model):
#     user = models.ForeignKey(User, verbose_name = "Пользователь", on_delete=models.CASCADE, related_name = "Whishlist_item", null=True)
#     event_name = models.CharField(max_length=255, verbose_name = "Название события")
#     event_date = models.DateTimeField(verbose_name = "Дата события", auto_now_add=False)
    
#     class Meta:
#          verbose_name = "Событие пользователя"
#          verbose_name_plural = "События пользователей"

# Модель настроек
class Settings(models.Model):
    start_message_text = models.TextField(verbose_name = "Текст сообщения для команды /start")
    start_message_image = models.ImageField(blank=True, upload_to='photo', verbose_name = "Изображение к команде /start")
    create_list_text = models.TextField(verbose_name = "Текст для создания ВИШ-листа")
    create_list_image = models.ImageField(blank=True, upload_to='photo', verbose_name = "Изображение для создания ВИШ-листа")
    after_create_list_text = models.TextField(verbose_name = "Текст после создания ВИШ-листа")
    error_create_list_text = models.TextField(verbose_name = "Текст на случай неправильного формата ввода ВИШ-листа")
    find_user_text = models.TextField(verbose_name = "Текст для поиска пользователя")
    error_find_user_text = models.TextField(verbose_name = "Текст на случай, если пользователь не найден")
    whats_next_text = models.TextField(verbose_name = "Текст для раздела 'Отправил, что дальше?'")

    def __str__(self):
        return "Настройки бота"
    
    class Meta:
         verbose_name = "Настройка"
         verbose_name_plural = "Настройки"

    def save(self, *args, **kwargs):
        # Ensure only one instance of this model is saved
        self.pk = 1
        super(Settings, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Disable deleting of this model instance
        pass

    @classmethod
    def load(cls):
        # Get the singleton instance or create it if it doesn't exist
        obj, created = cls.objects.get_or_create(pk=1)
        return obj