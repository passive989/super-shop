from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from .models import Category, Product, Review

from .forms import ReviewForm


class ShopListView(ListView):
    model = Product
    queryset = Product.objects.order_by("-created_at")
    template_name = 'pages/index.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(ShopListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('name')  
        return context  


class ProductDetailView(FormMixin, DetailView):
    model = Product
    template_name = 'pages/product_detail.html'
    form_class = ReviewForm
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']        
        context.update({
            'categories': Category.objects.order_by('name'),
            'review_list': Review.objects.filter(product = self.object.id),
            'review_form': ReviewForm(initial={'product': self.object.id })
        })        
        return context  

    def get_success_url(self):
        return reverse('product_detail', kwargs={'slug': self.object.slug})
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        review = Review()
        review.product = self.object
        review.author = self.request.user.username
        review.review = form.cleaned_data['review']
        review.save()
        messages.success(self.request, _('Your review submited successfuly!'))
        return super(ProductDetailView, self).form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, _('failed.'))
        return super(ProductDetailView, self,).form_invalid(form)

class CategoryList(ListView):
    model = Product
    template_name = 'pages/index.html'
    context_object_name = 'products'
    queryset = Category.objects.order_by('name') 

     
    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('name')  
        return context  


    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.all()
        slug = self.kwargs['slug']
        if slug:
            category = Category.objects.filter(slug=slug).first()
            queryset = queryset.filter(category=category.id)
        return queryset    



class SearchResultsListView(ListView): 
    model = Product 
    context_object_name = 'products' 
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('name')  
        return context  

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(name__icontains=query)
        )
