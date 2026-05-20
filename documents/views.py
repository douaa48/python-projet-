from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Document


@login_required
def documents_list(request):

    if request.method == "POST":
        title = request.POST.get("title")
        file = request.FILES.get("file")

        if title and file:
            Document.objects.create(
                user=request.user,
                title=title,
                file=file
            )

    documents = Document.objects.filter(user=request.user)

    return render(request, "frontend/documents/list.html", {
        "documents": documents
    })

@login_required
def delete_document(request, id):
    doc = Document.objects.filter(id=id, user=request.user).first()
    if doc:
        doc.delete()
    return redirect("documents")