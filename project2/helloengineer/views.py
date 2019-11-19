from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.views import generic
from .models import Group, Comment, Profile
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.generic.edit import ModelFormMixin

def index(request):
	return render(request,'helloengineer/index.html')
	
def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			new_user=form.save()
			input_username = form.cleaned_data['username']
			input_password = form.cleaned_data['enter_password']
			new_user = authenticate(username=input_username, password=input_password)
			if new_user is not None:
				login(request, new_user)
				return render(request,'helloengineer/userpage.html')
	else:
		form = SignUpForm()

	context = {'form':form}
	return render(request, 'helloengineer/signup.html', context)
	

#グループ一覧表示
class GroupList(generic.ListView):
	model=Group
	template_name = 'helloengineer/group_list.html'
	paginate_by=6
	
	def get_queryset(self):
		queryset=Group.objects.order_by('-created_at')
		keyword=self.request.GET.get('keyword')
		if keyword:
			queryset=queryset.filter(title__icontains=keyword)
		return queryset

#グループ作成
@login_required
def GroupCreate(request):
	form=GroupCreateForm(request.POST, request.FILES or None)
	
	if request.method=='POST' and form.is_valid():
		group = form.save(commit=False)
		group.create_user = request.user
		group.save()
		return redirect('helloengineer:group_list')

	context={
			'form':form
	}
	return render(request,'helloengineer/group_create.html',context)
		
#グループ詳細ページ
class ThreadView(ModelFormMixin, generic.DetailView):
	model = Group
	template_name = 'helloengineer/group_thread.html'
	form_class = CommentCreateForm

	def form_valid(self, form):
		group_pk = self.kwargs['pk']
		comment = form.save(commit=False)
		comment.create_user = self.request.user
		comment.post = get_object_or_404(Group, pk=group_pk)
		comment.save()
		return redirect('helloengineer:group_thread', pk=group_pk)
		
	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			self.object = self.get_object()
			return self.form_invalid(form)

#自分のページを表示
@login_required
def mypage(request, user_pk):
	mypage=get_object_or_404(User,pk=user_pk)
	
	return render(request,'helloengineer/mypage.html')

#別ユーザのページを表示
def userpage(request,user_pk):
	user=get_object_or_404(User,pk=user_pk)
	
	context={
		'user':user
	}
	return render(request,'helloengineer/userpage.html',context)
	
#プロフィールを更新
@login_required
def profileupdate(request,pk):
	profile=get_object_or_404(Profile,pk=pk)
	
	form=ProfileUpdateForm(request.POST, request.FILES or None, instance=profile)
	
	if request.method=='POST' and form.is_valid():
		profile = form.save(commit=False)
		profile.user = request.user
		form.save()
		return render(request,'helloengineer/mypage.html')
		
	context={
		'form':form
	}
	return render(request,'helloengineer/profileupdate.html',context)

#グループを削除
def delete_group(request, group_pk):
	group = get_object_or_404(Group, pk=group_pk)
	group.delete()
	return render(request,'helloengineer/mypage.html')
	
