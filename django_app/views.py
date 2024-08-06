from django.views.generic import TemplateView

from django_app.models import Item


class MenuView(TemplateView):
    template_name = 'menu.html'

    def get_context_data(self, **kwargs):
        context = super(MenuView, self).get_context_data(**kwargs)
        items = Item.objects.raw(
            f'''
            WITH RECURSIVE current AS (
                SELECT initial.id, initial.name, initial.menu_id, initial.parent_id
                FROM django_app_item as initial
                    LEFT JOIN (SELECT id FROM django_app_item WHERE parent_id=6 LIMIT 1) as children
                WHERE children.id is not null AND initial.id = children.id OR
                  children.id is null AND initial.id = 6
            
                UNION
                    SELECT sibling.id, sibling.name, sibling.menu_id, sibling.parent_id
                    FROM django_app_item sibling
                        JOIN current ON sibling.parent_id = current.parent_id 
                        OR sibling.parent_id is null and current.parent_id is null
            
                UNION
                    SELECT parent.id, parent.name, parent.menu_id, parent.parent_id
                    FROM django_app_item parent
                        JOIN current ON current.parent_id = parent.id
            
                )
            SELECT * FROM current;
            ''')

        context['items'] = items
        # TODO: [
        #     {
        #          name: '',
        #          children: [],
        #      },
        #     {
        #         name: '',
        #         children: [
        #             {'name': '',
        #              'children':[]
        #              }
        #         ]
        #     }
        # ]
        return context

