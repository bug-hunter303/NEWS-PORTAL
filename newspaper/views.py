from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView,CreateView
from django.urls import reverse_lazy
from newspaper.forms import ContactForm
from newspaper.models import Category, Post,Advertisement,OurTeam,Contact

from django.utils import timezone
from datetime import timedelta


class SidebarMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["popular_posts"] = Post.objects.filter(
            published_at__isnull = False , status = "active"
        ).order_by("-published_at")[:5]

        context["advertisement"] = (
            Advertisement.objects.all().order_by("-created_at").first()
        )

        return context


# Create your views here.

class HomeView(SidebarMixin,TemplateView):
    template_name = 'newsportal/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_post"] = (
            Post.objects.filter(published_at__isnull = False , status = "active").order_by("-published_at","-views_count").first()

        )

        context["trending_news"] = Post.objects.filter(
            published_at__isnull = False , status = "active"
        ).order_by("-views_count")[:4] # 5 ota samma dekhaune

        

        one_week_ago = timezone.now() - timedelta(days=7) # aaja ko time dekhi 7 days ghatako : to show last seven days ko news 
        context["weekly_top_posts"] = Post.objects.filter(
            published_at__isnull = False , status = "active", published_at__gte = one_week_ago # gte = greater than or equals to 
        ).order_by("-published_at","-views_count")[:5]

        context["breaking_news"] = Post.objects.filter(
            published_at__isnull = False, status = "active", is_breaking_news = True
        ).order_by("-published_at")[:3]


        return context      
    
class PostListView(SidebarMixin,ListView):
    model = Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull = False , status="active"
        ).order_by("-published_at")
    


        return context

class PostDetailView(SidebarMixin,DetailView):
    model = Post 
    template_name = "newsportal/detail/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        query = super().get_queryset() # Post.objects.all()
        query = query.filter(published_at__isnull = False , status = "active")
        return query
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_post = self.object 
        current_post.views_count += 1
        current_post.save()

        context["related_posts"] = (
            Post.objects.filter(
                published_at__isnull = False,
                status = "active",
                category = self.object.category,
            )
            .exclude(id = self.object.id)
            .order_by("-published_at","-views_count")[:2]
        )
        return context 
    
class AboutView(TemplateView):
    template_name = "newsportal/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["our_teams"] = OurTeam.objects.all()
        return context
    
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
    
class ContactCreateView(SuccessMessageMixin , CreateView):
    model = Contact 
    template_name = "newsportal/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")
    success_message = "Your message has been sent successfuly "

    def form_invalid(self , form):
        messages.error(
            self.request,
            "There was an error sending your message. Please check the form.",
        )
        return super().form_invalid(form)
    
class PostByCategoryView(SidebarMixin,ListView):
    model = Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull = False,
            status = "active",
            category__id = self.kwargs["category_id"],
        ).order_by("-published_at")
        return query
    
class CategoryListView(ListView):
    model = Category
    template_name = "newsportal/categories.html"
    context_object_name = "categories"