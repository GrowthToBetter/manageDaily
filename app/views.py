from datetime import datetime
from django.shortcuts import render, get_object_or_404

from app.forms import LoginForm
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.http import JsonResponse

from dotenv import load_dotenv

load_dotenv()
# Create your views here.
from django.shortcuts import render
from .models import Expense
from django.db.models import Sum
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    expenses = Expense.objects.filter(user=request.user)
    if(expenses.count() < 1):
        return redirect('add_expense')
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    categories = expenses.values('category').annotate(total=Sum('amount'))

    return render(request, 'expenses/dashboard.html', {
        'expenses': expenses,
        'total_expense': total_expense,
        'categories': categories,
    })
from django.shortcuts import render, redirect
from .forms import ExpenseForm

def add_expense(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()

    return render(request, 'expenses/add_expense.html', {'form': form})


def edit_expense(request, expense_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == "POST":
        # Mengambil data dari form atau query parameters
        title = request.POST.get('title')
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        notes = request.POST.get('notes')

        # Validasi input
        if not title or not category or not amount:
            return HttpResponseBadRequest("All fields are required!")

        # Perbarui data
        expense.title = title
        expense.category = category
        expense.amount = amount
        expense.date = date if date else expense.date  # Menjaga nilai default jika date kosong
        expense.notes = notes

        # Simpan perubahan ke database
        expense.save()

        # Redirect ke halaman dashboard setelah update
        return redirect('dashboard')

    # Jika bukan metode POST, tampilkan form pengeditan
    return render(request, 'expenses/edit.html', {
        'expense': expense,
    })
# Delete Expense view
def delete_expense(request, expense_id):
    if not request.user.is_authenticated:
        return redirect('login')

    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        # Delete the expense
        expense.delete()

        # Return a success message
        return JsonResponse({'message': 'Expense deleted successfully'}, status=200)

    return render(request, 'expenses/delete.html', {'expense': expense})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user, created = User.objects.get_or_create(username=username)
            if created:
                # Buat pengguna baru dengan password
                user.set_password(password)
                user.save()
                login(request, user)
                return redirect('/')
            else:
                # Autentikasi pengguna
                user = authenticate(request, username=username, password=password)
                if not user:
                    # Jika password salah, kembalikan pesan error
                    return render(request, 'login.html', {'error': 'Password salah!'})
                login(request, user)
                return redirect('/')  # Redirect ke halaman profil
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)  # Hapus sesi pengguna
    return redirect('login')  # Redirect ke halaman login

