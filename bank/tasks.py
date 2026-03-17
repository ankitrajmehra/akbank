from .models import BankAccount, Transaction, Loan

def credit_loan_amount(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        account = BankAccount.objects.get(id=loan.account.id)

        # Balance mein loan amount add karo
        account.balance += loan.amount
        account.save()

        # Transaction save karo
        Transaction.objects.create(
            user_id=loan.user.id,
            account=account,
            transaction_type='deposit',
            amount=loan.amount,
            balance_after=account.balance
        )
        print(f"✅ Loan credited: Rs.{loan.amount}")

    except Exception as e:
        print(f"❌ Error: {e}")