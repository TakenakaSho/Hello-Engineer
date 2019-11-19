from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

GENDER_CHOICES = (
	('1', '女性'),
	('2', '男性'),
	('3', '未設定'),
)

class Profile(models.Model):
	user_img = models.ImageField("アイコン", upload_to='helloengineer/users',blank=True, null=True)
	income = models.CharField("年収", max_length=15, default='未設定')
	gender = models.CharField("性別", max_length=3, choices=GENDER_CHOICES, blank=True, default=3)
	birthday = models.DateField("生年月日", blank=True, null=True)
	intro = models.TextField("自己紹介", max_length=400,blank=True, null=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE, default='未設定')
	
	@receiver(post_save, sender=User)
	def create_profile(sender, **kwargs):
		if kwargs['created']:
			user_profile = Profile.objects.get_or_create(user=kwargs['instance'])
	
	def __str__(self):
		return str(self.user)

class Group(models.Model):
	title = models.CharField('グループ名',max_length=50,validators=[MinLengthValidator(1)])
	group_img = models.ImageField('イメージ画像', upload_to='helloengineer/groups',blank=True, null=True)
	create_user = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField('作成日', default=timezone.now)
	
	def __str__(self):
		return self.title

class Comment(models.Model):
	text = models.TextField('本文')
	post = models.ForeignKey(Group, verbose_name='紐づくグループ', on_delete=models.CASCADE)
	created_at = models.DateTimeField('作成日', default=timezone.now)
	create_user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.text[:10]

