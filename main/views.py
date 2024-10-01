from django.shortcuts import render
from django.views.generic import TemplateView


# from django.http import HttpResponseRedirect
# from .forms import UploadFileForm
#
# # Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file
#
#
# def upload_file(request):
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES["file"])
#             return HttpResponseRedirect("/success/url/")
#     else:
#         form = UploadFileForm()
#     return render(request, "upload.html", {"form": form})



class HomePageView(TemplateView):
    template_name = 'main/home.html'
