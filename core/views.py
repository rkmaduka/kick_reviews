from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from .models import *
from django.core.exceptions import PermissionDenied
from .forms import *
# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

class ReviewCreateView(CreateView):
  model = Review
  template_name = "review/review_form.html"
  fields = ['sneaker', 'review']
  success_url = reverse_lazy('review_list')

def form_valid(self, form):
      form.instance.user = self.request.user
      return super(ReviewCreateView, self).form_valid(form)

class ReviewListView(ListView):
    model = Review
    template_name = "review/review_list.html"

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'review/review_detail.html'
    
def get_context_data(self, **kwargs):
    context = super(ReviewDetailView, self).get_context_data(**kwargs)
    review = Review.objects.get(id=self.kwargs['pk'])
    comments = Comments.objects.filter(review=review)
    context['comments'] = comments
    user_comments = Comments.objects.filter(review=review, user=self.request.user)
    context['user_comments'] = user_comments
    return context
        
class ReviewUpdateView(UpdateView):
    model = Review
    template_name = 'review/review_form.html'
    fields = ['sneaker', 'review']
    
    def get_object(self, *args, **kwargs):
        object = super(ReviewUpdateView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object
    
class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'review/review_confirm_delete.html'
    success_url = reverse_lazy('review_list')
    
    def get_object(self, *args, **kwargs):
        object = super(ReviewDeleteView, self).get_object(*args, **kwargs)
        if object.user != self.request.user 
            raise PermissionDenied
        return object 
        
class CommentsCreateView(CreateView):
    model = Comments
    template_name = "comments/comments_form.html"
    fields = ['text']
    
    def get_success_url(self):
        return self.object.review.get_absolute_url()
        
    def form_valid(self, form):
        review = Review.objects.get(id=self.kwargs['pk'])
        if Comments.objects.filter(review=review, user=self.request.user.exists():
            raise PermissionDenied() 
        form.instance.user = self.request.user
        form.instance.review = Review.objects.get(id=self.kwargs['pk'])
        return super(CommentsCreateView, self).form_valid(form)
        
class CommentsUpdateView(UpdateView):
    model = Comments
    pk_url_kwarg = 'comments_pk'
    template_name = 'comments/comments_form.html'
    fields = ['text']
    
    def get_success_url(self):
        return self.object.review.get_absolute_url()
    
    def get_object(self, *args, **kwargs):
            object = super(CommentsUpdateView, self).get_object(*args, **kwargs)
            if object.user != self.request.user:
                raise PermissionDenied()
            return object 
            
class CommentsDeleteView(DeleteView):
    model = Comments
    pk_url_kwarg = 'comments_pk'
    template_name = 'comments/comments_confirm_delete.html'
    
    def get_success_url(self):
        return self.object.review.get_absolute_url()
    
    def get_object(self, *args, **kwargs):
        object = super(CommentsDeleteView, self)get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object 
        
class VoteFormView(FormView):
    form_class = VoteForm
    
    def form_valid(self, form):
        user = self.request.user
        review = Review.objects.get(pk=form.data['review])
        try:
            comments = Comments.objects.get(pk=form.data["comments"])
            prev_votes = Vote.objects.filter(user=user, comments=comments)
            has_voted = (prev_votes.count()>0)
            if not has_voted:
                Vote.objects.create(user=user, comments=comments)
            else:
                prev_votes[0].delete()
            return redirect(reverse('review_detail', args=[form.data["review]]))
        except:
            prev_votes = Vote.objects.filter(user=user, review=review)
            has_voted = (prev_votes.count()>0)
            if not has_voted:
                Vote.objects.create(user=user, review=review)
            else:
                prev_votes[0].delete()
        return redirect('review_list')
      
      class UserDetailView(DetailView):
          model = User
          slug_field = 'username'
          template_name = 'user/user_detail.html'
          context_object_name = 'user_in_view'
          
          def get_context_data(self, **kwargs):
              context = super(UserDetailView, self).get_context_data(**kwargs)
              user_in_view = User.objects.get(username=self.kwargs['slug']
              reviews = Review.objects.filter(user=user_in_view)
              context['reviews'] = reviews
              comments = Comments.objects.filter(user=user_in_view)
              context['comments'] = comments
              return context
              
        class UserUpdateView(UpdateView):
            model = User
            slug_field = "username"
            template_name = "user/user_form.html"
            fields = ['email', 'first_name', 'last_name']
            
            def get_success_url(self):
                return reverse('user_detail ', args=[self.request.user.username]
                
            def get_object(self, *args, **kwargs):
                object = super(UserUpdateView, self).get_object(*args, **kwargs)
                if object != self.request.user:
                    raise PermissionDenied
                return object 
                