
from rest_framework import serializers
from .models import Transactions
from django.db import transaction


from fpdf import FPDF

from django.core.mail import EmailMessage
from api import settings



def generate_pdf(instance):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Optional: Add the bank logo

    pdf.cell(200, 10, txt="Bank of algeria", ln=True, align='C')

    
    pdf.cell(200, 10, txt="Transaction Receipt", ln=True, align='C')
    # Add transaction details
    pdf.cell(200, 10, txt=f"NIN: {instance.nin}", ln=True)
    pdf.cell(200, 10, txt=f"Name: {instance.first_name} {instance.last_name}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {instance.email}", ln=True)
    pdf.cell(200, 10, txt=f"Municipal: {instance.municipal}", ln=True)
    pdf.cell(200, 10, txt=f"Wilaya: {instance.wilaya}", ln=True)
    pdf.cell(200, 10, txt=f"Payment Code: {instance.payment_code}", ln=True)
    pdf.cell(200, 10, txt=f"Payment Date: {instance.payment_date.strftime('%Y-%m-%d')}", ln=True)

    # Save to a variable
    # pdf_output = pdf.output(dest='S').encode('latin1')
    
    file_path = f"transactions/{instance.payment_code}.pdf"
    pdf.output(file_path, 'F')
    binary_pdf = open(file_path, 'rb').read()
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
            "file" : {"required": False}
        }
        
        
    def create(self, validated_data):
        with transaction.atomic():
            transa = Transactions.objects.create(**validated_data)
            
            transa.save()
            
            try:
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
            except Exception as e:
                
                transa.delete()
                raise serializers.ValidationError({"error": str(e)})
            
            
            
            
            
            return transa

        
    