from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from . import SQLite
from os import listdir
from os.path import isfile, join
import json
table,db = "",""
# print('-----{}'format(os.getcwd()))
User = get_user_model()
class HomeView(View):
    def get(self, request, *args, **kwargs):
        global db,table
        if 'mySelect' in request.GET:
            db = request.GET['mySelect']
            print('select ---- {}'.format(request.GET['mySelect']))
        elif 'myTable' in request.GET:
            table = request.GET['myTable']
            print('table ---- {}'.format(request.GET['myTable']))
        return render(request, 'charts.html', {})

def get_data(request, *args, **kwargs):
    print(request.GET['mySelect'])
    data = {
        "mySelect": request.GET['mySelect'],
    }
    return JsonResponse(data) # http response

def get_bg(request):
    context = {}
    template = "bg.html"
    return render(request, template, context) # http response

class DataView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html', {})

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        global table, db
        tablenum = []
        mypath = 'C:/Users/nick/chart/sqlite'
        dbfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for f in dbfiles:
            getlist = []
            a = SQLite.SQLite('C:/Users/nick/chart/sqlite/{}'.format(f))
            a.connect()
            a.cursor()
            gettables = a.table()
            for t in gettables:
                getlist.append(t[1])
            a.close()
            tablenum.append(len(getlist))
        qs_count = User.objects.all().count()
        labels = []
        default_items = []
        tablelist = []
        columnlist = []
        if db:
            sql = SQLite.SQLite('C:/Users/nick/chart/sqlite/{}'.format(db))
            sql.connect()
            sql.cursor()
            alltable = sql.table()
            for tname in alltable:
                tablelist.append(tname[1])
            if not table: table = tablelist[0]
            gettable = "'"+table+"'"
            alldata = sql.select(gettable)
            for i in alldata:
                labels.append(i[0])
                default_items.append(i)
            columnlist = sql.getcolname(gettable)
            sql.close()
        data = {
            "dbfiles": dbfiles,
            "labels": labels,
            "default": default_items,
            "tables": tablelist,
            "table": table,
            "num": tablenum,
            "columns": columnlist,
            "db": db,
        }
        table = ""
        return Response(data)

