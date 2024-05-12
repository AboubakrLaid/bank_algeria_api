
from rest_framework import serializers
from .models import Transactions
from django.db import transaction


from fpdf import FPDF

from api import settings
from datetime import  timezone , timedelta
from django.core.mail import EmailMessage



def generate_pdf(instance):
    print("generatting pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Optional: Add the bank logo

    pdf.cell(200, 10, txt="Bank of algeria", ln=True, align='C')

    
    pdf.cell(200, 10, txt="Transaction Receipt", ln=True, align='C')
    # Add transaction details
    #! the point after each string is used to facilitate the extracting of the text from the pdf
    pdf.cell(200, 10, txt=f"NIN: {instance.nin}.", ln=True)
    pdf.cell(200, 10, txt=f"First Name: {instance.first_name}.", ln=True)
    pdf.cell(200, 10, txt=f"Last Name: {instance.last_name}.", ln=True)
    pdf.cell(200, 10, txt=f"Email: {instance.email}.", ln=True)
    pdf.cell(200, 10, txt=f"Wilaya: {instance.wilaya}.", ln=True)
    pdf.cell(200, 10, txt=f"Payment Code: {instance.payment_code}.", ln=True)
    algeria_offset = timedelta(hours=1)

    # Convert instance.date_created to a timezone-aware datetime object
    adjusted_time = instance.payment_date.astimezone(timezone(algeria_offset))
    pdf.cell(200, 10, txt=f"Payment Date: {adjusted_time.strftime("%Y-%m-%d %H:%M:%S")}", ln=True)

    # Save to a variable
    # pdf_output = pdf.output(dest='S').encode('latin1')
    
    file_path = f"transactions/{instance.payment_code}.pdf"
    pdf.output(file_path, 'F')
    binary_pdf = open(file_path, 'rb').read()
    print("pdf generated")
    return binary_pdf
    

def send_transaction_email(subject, message, from_email, recipient_list, pdf_attachment=None):
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=recipient_list
    )

    if pdf_attachment is not None:
        # pdf_attachment should be a tuple of (filename, content, mimetype)
        email.attach(pdf_attachment[0], pdf_attachment[1], pdf_attachment[2])

    email.send()






class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'
        extra_kwargs = {
            "file" : {"required": False},
            "payment_code": {"read_only": True},
        }
      
        
        
    def create(self, validated_data):
        with transaction.atomic():
            
            
            try:
                transa = Transactions.objects.create(**validated_data)
                
                pdf_content = generate_pdf(transa)
                pdf_filename = f"{transa.payment_code}.pdf"
                pdf_mimetype = 'application/pdf'
                
                send_transaction_email(
                    subject="Your Payment Receipt",
                    message="Here is your payment receipt from the Bank of Algeria",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[transa.email],
                    pdf_attachment=(pdf_filename, pdf_content, pdf_mimetype)
                )
                transa.file = pdf_filename
                transa.save()
            except Exception as e:
                transa.delete()
                raise serializers.ValidationError({"error": e})
            return transa
        
        
class TransactionValidationSerializer(serializers.Serializer):
    nin = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    payment_code = serializers.CharField()
    
    def validate(self, data):
        nin = data.get("nin")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        payment_code = data.get("payment_code")
        
        try:
            Transactions.objects.get(nin=nin, first_name=first_name, last_name=last_name, payment_code=payment_code)
        except Transactions.DoesNotExist:
            raise serializers.ValidationError({"error": "Transaction not found"})
        return data

        
    