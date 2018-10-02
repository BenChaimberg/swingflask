from flask import redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import current_user


class CustomModelView(ModelView):
    column_display_pk = True
    list_template = 'admin/right_links_model.html'

    def is_accessible(self):
        return current_user.is_authenticated()


class ProductModelView(CustomModelView):
    column_default_sort = 'id'
    column_filters = ('id',)
    can_export = True
    form_columns = [
        'id',
        'title',
        'demo',
        'text',
        'directions',
        'forms_us',
        'forms_can',
        'category',
        'brand'
    ]


class CategoryModelView(CustomModelView):
    column_default_sort = 'id'
    column_filters = ('id',)
    can_export = True
    form_columns = [
        'id',
        'category',
        'name',
    ]


class BrandModelView(CustomModelView):
    column_default_sort = 'id'
    column_filters = ('id',)
    can_export = True
    form_columns = [
        'id',
        'brand',
        'name',
    ]


class BrochureModelView(CustomModelView):
    column_default_sort = ('xdate', True)
    column_filters = ('idbrochure', 'language', 'xdate',)
    can_export = True
    form_columns = [
        'contact',
        'email',
        'address',
        'city',
        'province',
        'postal_code',
        'country',
        'xdate',
        'language',
    ]


class NewsletterModelView(CustomModelView):
    column_default_sort = 'id'
    column_filters = ('id',)
    can_export = True
    form_columns = [
        'email'
    ]


class MessageModelView(CustomModelView):
    column_default_sort = 'IDmessage'
    column_filters = ('IDmessage', 'mdate', 'last_rdate', 'notifyemail',)
    can_export = True
    form_columns = [
        'subject',
        'name',
        'email',
        'notifyemail',
        'mdate',
        'message',
        'last_rdate',
    ]


class ReplyModelView(CustomModelView):
    column_default_sort = 'IDreply'
    column_filters = ('IDmessage', 'IDreply', 'rdate', 'notifyemail',)
    can_export = True
    form_columns = [
        'IDmessage',
        'subject',
        'name',
        'email',
        'notifyemail',
        'message',
        'rdate',
    ]


class InfoTableModelView(CustomModelView):
    column_default_sort = 'id'
    column_filters = ('id', 'productid',)
    can_export = True
    form_columns = [
        'id',
        'productid',
        'size',
        'quantity',
        'sizefr',
        'quantityfr'
    ]


class InfoListModelView(CustomModelView):
    column_default_sort = 'id'
    column_filters = ('id', 'productid',)
    can_export = True
    form_columns = [
        'id',
        'productid',
        'infolist',
        'infolistfr'
    ]


class CustomFileAdmin(FileAdmin):
    list_template = 'admin/right_links_file.html'
    can_upload = False
    can_delete = False
    can_delete_dirs = False
    can_mkdir = False
    can_rename = False

    def is_accessible(self):
        return current_user.is_authenticated()


class ProtectedAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated():
            return redirect(url_for('login'))
        return super(ProtectedAdminIndexView, self).index()
