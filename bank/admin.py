from django.contrib import admin
from .models import user, BankAccount, Loan, Transaction, Suggestion
from .tasks import credit_loan_amount
import threading

def schedule_loan_credit(loan_id, delay_seconds=600):
    # 10 minute baad credit karo
    timer = threading.Timer(delay_seconds, credit_loan_amount, args=[loan_id])
    timer.start()
    print(f"⏳ Loan {loan_id} scheduled — {delay_seconds} seconds mein credit hoga!")

@admin.register(user)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
    search_fields = ['email']

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['account_no', 'name', 'account_type', 'branch', 'balance', 'user']
    search_fields = ['account_no', 'name']
    list_filter = ['account_type']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['user', 'loan_type', 'amount', 'duration_months', 'status', 'applied_date']
    list_filter = ['status', 'loan_type']
    search_fields = ['user__email']
    list_editable = ['status']
    # anKIt shRhwTehdwwkjw@hsg#hsg$hbdyedhhd

    def save_model(self, request, obj, form, change):
        # Pehle check karo — pehle kya status tha
        if change:  # Edit ho raha hai
            old_loan = Loan.objects.get(id=obj.id)
            old_status = old_loan.status
        else:
            old_status = None

        # Save karo
        super().save_model(request, obj, form, change)

        # Agar abhi approved kiya — pehle pending tha
        if obj.status == 'approved' and old_status != 'approved':
            # 10 minute = 600 seconds baad credit karo ✅
            schedule_loan_credit(obj.id, delay_seconds=600)
            self.message_user(
                request,
                f"✅ Loan Approved! Rs.{obj.amount} 10 minutes mein "
                f"{obj.account.name} ke account mein credit ho jayega!"
            )

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'account', 'transaction_type',
                    'amount', 'balance_after', 'date']
    list_filter = ['transaction_type']
    search_fields = ['user__email']

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'category', 'rating', 'date']
    list_filter = ['category', 'rating']
    search_fields = ['name', 'email']
    readonly_fields = ['name', 'email', 'category',
                       'rating', 'message', 'date']