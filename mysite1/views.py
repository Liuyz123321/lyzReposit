import csv
import string

from bs4 import BeautifulSoup
from django.http import HttpResponse
from sphinx.util import requests
from django.shortcuts import render

def test_html(request):
    # from django.template import loader
    # t = loader.get_template('test_html.html')
    # html = t.render()

    dic = {'username': '111', 'age': 18}
    return render(request, 'test_html.html', dic)

def getdata(request,province,city):
    URL = "https://%s.ke.com/ershoufang/%s/pg" % (province, city)
    csvFileName = "%s_%s.csv" % (province, city)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=csvFileName'
    list = []
    Ave = []
    class house:
        def __init__(self):
            self.URL = URL
            self.ave = 0
            self.array_range = []
            for num in range(1, 5):
                self.array_range.append(num)
            self.header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
        def get_data(self):
            csvfile = open(csvFileName, 'w', newline='')
            writer = csv.writer(response)
            sum = 0
            coun = 0
            ave = 0.0
            for num in self.array_range:
                num = str(num)
                html = requests.get(self.URL + num, headers=self.header);
                soup = BeautifulSoup(html.text, "html.parser");
                name = soup.select("div.priceInfo > div.unitPrice > span ")
                for n in name:
                    # n = (string)n
                    # n = n.match('^.*(\d{1,5},\d{1,5})')
                    writer.writerow(n)
                    # list.append(n.search('(\d{1,5})'))
                    list.append(n.text)
                    # global sum
                    # print(type(int(n.text.replace('元/平','').replace(',',''))))
                    sum = sum + int(n.text.replace('元/平','').replace(',',''))
                    coun+=1
                    # print(sum)
                    # print(n.text)
            ave = sum / coun
            # global Ave
            # self.ave = sum/coun
            # print(Ave)
            Ave.append(ave)
            csvfile.close()

    cls = house()
    cls.get_data()
    # print(Ave)
    return render(request,'getdata.html',locals())


def getdata_csv(request, province, city):
    URL = "https://%s.ke.com/ershoufang/%s/pg" % (province, city)
    csvFileName = "%s_%s.csv" % (province, city)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=%s'%csvFileName
    list = []
    class house:
        def __init__(self):
            self.URL = URL
            self.array_range = []
            for num in range(1, 5):
                self.array_range.append(num)
            self.header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

        def get_data(self):
            csvfile = open(csvFileName, 'w', newline='')
            writer = csv.writer(response)
            for num in self.array_range:
                num = str(num)
                html = requests.get(self.URL + num, headers=self.header);
                soup = BeautifulSoup(html.text, "html.parser");
                name = soup.select("div.priceInfo > div.unitPrice > span")
                for n in name:
                    writer.writerow(n)
                    list.append(n)
            csvfile.close()
    cls = house()
    cls.get_data()

    return response
    # return render(request,'getdata.html',locals())