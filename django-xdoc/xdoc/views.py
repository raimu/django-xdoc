from django.shortcuts import render


def main(request):
    return render(request, "xdoc/main.html")