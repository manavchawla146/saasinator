from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import IdeaHistory
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
from .forms import RegisterForm, CustomLoginForm

# Initialize Gemini
genai.configure(api_key="AIzaSyA5-xrQzH4KInOBkFuvHmX1Yzwzvr-0tbY")

@login_required
@csrf_exempt
def submit_idea(request):
    if request.method == "POST":
        idea = request.POST.get("inputField")
        vibe = request.POST.get("vibe")
        output = request.POST.get("output")

        if not idea or not vibe or not output:
            return JsonResponse({"status": "error", "output": "Missing required fields"})

        try:
            # Save to database
            history_item = IdeaHistory.objects.create(
                user=request.user,
                idea=idea,
                vibe=vibe,
                output=output
            )
            return JsonResponse({
                "status": "success",
                "output": output,
                "history_id": history_item.id
            })
        except Exception as e:
            return JsonResponse({"status": "error", "output": f"Database error: {str(e)}"})
    return JsonResponse({"status": "error", "output": "Invalid request method"})

@login_required
def index(request):
    history = IdeaHistory.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "index.html", {"history": history})

@login_required
def history(request):
    history = IdeaHistory.objects.filter(user=request.user).order_by("-created_at").values('id', 'idea', 'vibe')
    return JsonResponse(list(history), safe=False)

@login_required
def get_history_detail(request, history_id):
    try:
        history_item = IdeaHistory.objects.get(id=history_id, user=request.user)
        return JsonResponse({
            "status": "success",
            "idea": history_item.idea,
            "vibe": history_item.vibe,
            "output": history_item.output
        })
    except IdeaHistory.DoesNotExist:
        return JsonResponse({"status": "error", "output": "History item not found"})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                return redirect("index")
    else:
        form = CustomLoginForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")