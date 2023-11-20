from django.db import models
from django.urls import reverse
from django.conf import settings

class user (models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=30)
    year = models.IntegerField()


class FoodTypes(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'fcategory'
        verbose_name_plural = 'fcategories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('healthbutler:food_list_by_fcategory',
                       args=[self.slug])


class Foods(models.Model):
    fcategory = models.ForeignKey(FoodTypes,
                                 related_name='food', on_delete=models.CASCADE,)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True,default='')
    serving = models.CharField(max_length=200)
    calories = models.PositiveIntegerField()
    fat = models.PositiveIntegerField()
    carbs = models.PositiveIntegerField()
    fiber = models.PositiveIntegerField()
    protein = models.PositiveIntegerField()


    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('healthbutler:food_detail',
                       args=[self.id, self.slug])


class CheckIn(models.Model):
    default_item = "Daily Check In"
    eat_breakfast = "Eat Breakfast"
    exercise = "Exercise"
    drink_more_water = "Drink More Water"
    early_bedtime = "Early Bedtime"
    go_to_toilet = "Go To Toilet"

    user_id = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=200)
    check_in_day = models.PositiveIntegerField()
    days = models.PositiveIntegerField()


    class Meta:
        ordering = ('id',)
        index_together = (('user_id', 'name'),)


    def get_icon(self):
        icon_map = {
            self.eat_breakfast: "icon/3.png",
            self.exercise: "icon/5.png",
            self.drink_more_water: "icon/6.png",
            self.early_bedtime: "icon/2.png",
            self.go_to_toilet: "icon/4.png",
        }
        return icon_map.get(self.name, "icon/1.png")


class QuestionAndAnswer(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    content = models.TextField()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE)
    weight = models.IntegerField(default=0,blank=True,null=True)
    height = models.IntegerField(default=0,blank=True,null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
