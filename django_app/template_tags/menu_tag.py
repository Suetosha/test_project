from pprint import pprint

from django import template

from django_app.models import Item
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    active_menu_item = context['path'].split('/')[-1]
    items = get_items_from_db(menu_name, active_menu_item)
    items_tree = get_menu_tree(items, path='/menu/')
    rendered_items_tree = render_menu(items_tree)
    return rendered_items_tree


def get_items_from_db(menu_name, active_menu_item):
    items = Item.objects.raw(
        f'''
            WITH RECURSIVE current AS (
                SELECT initial.id, initial.name, initial.menu_id, initial.parent_id,  initial.parent_id AS level
                FROM django_app_item as initial
                    LEFT JOIN (SELECT id 
                               FROM django_app_item WHERE parent_id=(SELECT id FROM django_app_item WHERE name="{active_menu_item}") LIMIT 1) as children
                WHERE children.id is not null AND initial.id = children.id OR
                  children.id is null AND initial.id = (SELECT id FROM django_app_item WHERE name="{active_menu_item}")
    
                UNION
                    SELECT sibling.id, sibling.name, sibling.menu_id, sibling.parent_id, current.level
                    FROM django_app_item sibling
                        JOIN current ON sibling.parent_id = current.parent_id
                        OR sibling.parent_id is null and current.parent_id is null
    
                UNION
                    SELECT parent.id, parent.name, parent.menu_id, parent.parent_id, current.level - 1
                    FROM django_app_item parent
                        JOIN current ON current.parent_id = parent.id
    
                )
            SELECT * FROM current;
        ''')

    items = list(reversed([i for i in items]))

    items = [{'id': i.id, 'name': i.name, 'menu_id': i.menu_id, 'parent_id': i.parent_id} for i in items]
    return items


def get_menu_tree(items_list: list, menu=None, parent_id=None, path='/'):
    if menu is None:
        menu = []

    for item in items_list:
        if item['parent_id'] == parent_id:
            item['path'] = path + item['name'] + '/'
            children = get_menu_tree(items_list, parent_id=item['id'], path=item['path'])
            if children:
                item['children'] = children
            menu.append(item)
    menu = sorted(menu, key=lambda i: i['name'])
    return menu


def render_menu(menu):
    def render_item(item):
        html = f'<li><a href="{item["path"]}">{item["name"]}</a>'

        if 'children' in item and item['children']:
            html += '<ul>'
            for child in item['children']:
                html += render_item(child)
            html += '</ul>'

        html += '</li>'
        return html

    html = '<ul>'
    for menu_item in menu:
        html += render_item(menu_item)
    html += '</ul>'

    return mark_safe(html)
