from datetime import datetime, timedelta, timezone


class RedeemDetails:
    def __init__(self, json_redeem_details: dict) -> None:
        if json_redeem_details is not None:
            self.email = json_redeem_details.get(
                "email", "Error retrieving payment email")
            self.payment_method = json_redeem_details.get(
                "payment_method", "Error retrieving payment method")
        else:
            self.email = "No email detected"
            self.payment_method = "No payment method found"


class Transaction:
    def __init__(self, json_transaction: dict) -> None:
        self.uuid = json_transaction.get(
            "uuid", "Error retrieving transaction UUID")
        self.status = json_transaction.get(
            "status", "Error retrieving transaction status")
        self.payment_method = json_transaction.get(
            "payment_method", "Payment method not found")
        self.email = json_transaction.get(
            "email", "No redeem email found.")
        self.amount = json_transaction.get(
            "money_amount", "Error retrieving payment amount")

        self.redeem_date = datetime.strptime(
            json_transaction.get("date").replace("Z", "UTC"), "%Y-%m-%dT%H:%M:%S.%f%Z")

        payment_date = json_transaction.get("payment_date")

        if payment_date is None:
            self.payment_date = self.redeem_date + timedelta(days=9)
        elif type(payment_date) is str:
            self.payment_date = datetime.strptime(
                payment_date.replace("Z", "UTC"), "%Y-%m-%dT%H:%M:%S.%f%Z")
        else:
            self.payment_date = datetime.now(timezone.utc)

        if self.status == "paid":
            self.is_paid = True
        else:
            self.is_paid = False


class Transactions:
    def __init__(self, json_transactions) -> None:
        self.transactions = []
        self.pending_payments = 0
        self.paid = 0
        for transaction in json_transactions:
            self.transactions.append(Transaction(transaction))

        self.total_transactions = len(self.transactions)
        for transaction in self.transactions:
            if transaction.is_paid:
                self.paid += 1
            else:
                self.pending_payments += 1
    
    def get_transactions(self)->list[Transaction]:
        return self.transactions
