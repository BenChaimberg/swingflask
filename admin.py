from flask import redirect, url_for
from flask.ext.admin import AdminIndexView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.login import current_user


class CustomModelView(ModelView):
    column_display_pk = True
    list_template = 'admin/right_links_model.html'

    def is_accessible(self):
        return current_user.is_authenticated()


class ProductModelView(CustomModelView):
    column_default_sort = 'id'
    column_filters = ('id',)
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
    form_columns = [
        'id',
        'category',
        'name',
    ]


class BrandModelView(CustomModelView):
    column_default_sort = 'id'
    column_filters = ('id',)
    form_columns = [
        'id',
        'brand',
        'name',
    ]


class BrochureModelView(CustomModelView):
    column_default_sort = 'idbrochure'
    column_filters = ('idbrochure', 'language',)
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
    form_columns = [
        'email'
    ]


class MessageModelView(CustomModelView):
    column_default_sort = 'IDmessage'
    column_filters = ('IDmessage', 'mdate', 'last_rdate', 'notifyemail',)
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
    form_columns = [
        'id',
        'productid',
        'size',
        'quantity'
    ]


class InfoListModelView(CustomModelView):
    column_default_sort = 'id'
    column_filters = ('id', 'productid',)
    form_columns = [
        'id',
        'productid',
        'infolist'
    ]


class CustomFileAdmin(FileAdmin):
    list_template = 'admin/right_links_file.html'

    def git_commit(self, name):
        bashCommand = 'git commit -m "admin_edit_' + str(name) + '"'
        import subprocess
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output

    def git_add(self, name):
        bashCommand = 'git add ' + str(name)
        import subprocess
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output

    def git_rm(self, name):
        bashCommand = 'git rm ' + str(name)
        import subprocess
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output

    def on_file_upload(self, full_path, dir_base, filename):
        self.git_add(filename)
        self.git_commit(filename)

    def is_accessible(self):
        return current_user.is_authenticated()


class ProtectedAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated():
            return redirect(url_for('login'))
        return super(ProtectedAdminIndexView, self).index()
