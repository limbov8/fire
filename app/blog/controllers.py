from flask.views import MethodView
from flask import render_template, make_response, redirect, url_for, flash

class BlogIndex(MethodView):
    def get(self):
        return "get index"

    def post(self):
        pass

class BlogView(MethodView):
    def get(self, id):
        return render_template('blog/view.html', id=id)

    def post(self):
        pass


class BlogEdit(MethodView):
    def get(self, id):
        return "edit" + id

    def post(self):
        pass


class BlogDelete(MethodView):
    def post(self):
        pass

