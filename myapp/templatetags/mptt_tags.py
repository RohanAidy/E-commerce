from django import template
from django.utils.safestring import mark_safe
from mptt.templatetags.mptt_tags import cache_tree_children

register = template.Library()

def recursive_category_tree(categories):
    """
    Recursively render category tree for MPTT
    """
    html = ''
    for category in categories:
        html += f'''
        <div class="category-node" data-level="{category.level}">
            <div class="category-item">
                {'<img src="' + category.image.url + '" alt="' + category.name + '" class="category-icon">' if category.image else '<div class="category-icon-placeholder"><i class="fas fa-book"></i></div>'}
                <div class="category-info">
                    <h3>
                        <a href="/category/{category.id}/">
                            {category.name}
                        </a>
                    </h3>
                    {'<p>' + category.description[:50] + '...</p>' if category.description else ''}
                </div>
                <div class="category-stats">
                    <span class="books-count">
                        <i class="fas fa-book"></i>
                        {category.products.count()} books
                    </span>
                    {f'<span class="subcategory-count"><i class="fas fa-sitemap"></i> {category.get_descendant_count()} subcategories</span>' if category.get_descendant_count() > 0 else ''}
                </div>
            </div>
        '''
        
        if category.get_children():
            html += '<div class="subcategories">'
            for child in category.get_children():
                html += f'''
                <div class="subcategory-item">
                    <a href="/category/{child.id}/" class="subcategory-link">
                        <i class="fas fa-angle-right"></i>
                        {child.name}
                    </a>
                    <span class="subcategory-count">({child.products.count()})</span>
                    {f'<span class="has-children"><i class="fas fa-chevron-down"></i></span>' if child.get_children() else ''}
                </div>
                '''
            html += '</div>'
        
        html += '</div>'
    
    return mark_safe(html)

@register.simple_tag
def category_tree():
    """
    Display full category tree using MPTT
    """
    from myapp.models import category
    categories = category.objects.root_nodes()
    return recursive_category_tree(categories)
