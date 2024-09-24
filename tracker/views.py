from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .models import Transaction
from matplotlib.figure import Figure
from io import BytesIO
import base64

def index(request):
    transactions = Transaction.objects.all()
    graph = generate_expense_graph()  # Generate the expense graph
    return render(request, 'tracker/index.html', {'transactions': transactions, 'graph': graph})

def add_transaction(request):
    if request.method == 'POST':
        transaction_type = request.POST.get('type')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        description = request.POST.get('description')
        date = timezone.now()  # Use timezone-aware datetime

        # Create and save the transaction
        Transaction.objects.create(
            type=transaction_type,
            amount=amount,
            category=category,
            description=description,
            date=date
        )
        return redirect('index')  # Redirect to the main page after saving
    return render(request, 'tracker/add_transaction.html')

def generate_expense_graph():
    transactions = Transaction.objects.filter(type='expense')
    categories = {}
    
    for transaction in transactions:
        categories[transaction.category] = categories.get(transaction.category, 0) + float(transaction.amount)

    fig = Figure()
    ax = fig.subplots()
    ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
    ax.set_title('Expenses by Category')

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return graph

def chart_view(request):
    graph = generate_expense_graph()  # Generate the graph
    return render(request, 'tracker/chart.html', {'graph': graph})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Redirect to the index page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'tracker/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to the index page after logout
