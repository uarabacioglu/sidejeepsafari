# from django.shortcuts import get_object_or_404
# from invoices.models import InvoiceModel
# from currencies.models import EfektifDovizModeli
# from bookings.models.booking_model import BookingModel


# def create_invoice(booking_uuid):
#     booking = get_object_or_404(BookingModel, booking_uuid=booking_uuid)
#     tour_date = booking.tour_date

#     try:
#         efektif_data = EfektifDovizModeli.objects.get(created_at__date=tour_date)
#     except EfektifDovizModeli.DoesNotExist:
#         return None

#     usd_to_tl = efektif_data.usd_to_tl
#     exchange_rate_float = float(usd_to_tl)
#     booking_price_usd = float(booking.price.split(" ")[0])
#     price_tl_with_tax = booking_price_usd * exchange_rate_float
#     tax_rate = 20.00
#     price_tl_without_tax = price_tl_with_tax / (1 + (tax_rate / 100))
#     kdv = price_tl_with_tax - price_tl_without_tax

#     invoice = InvoiceModel(
#         booking=booking,
#         tour_date=tour_date,
#         booking_ref=booking.booking_ref,
#         tour_name=booking.tour_name,
#         traveller_name=f"{booking.traveller_first_name} {booking.traveller_last_name}",
#         total_price_usd_with_tax=booking_price_usd,
#         usd_to_tl_currency=exchange_rate_float,
#         total_price_tl_with_tax=price_tl_with_tax,
#         tax_rate=tax_rate,
#         total_price_tl_without_tax=price_tl_without_tax,
#         kdv=kdv,
#     )
#     invoice.save()

# # TODO invoice app için kullan
# from decimal import Decimal
# from django.conf import settings
# from django.core.mail import EmailMessage
# from django.shortcuts import get_object_or_404
# from fpdf import FPDF
# from bookings.models.booking_model import BookingModel
# import logging

# # Setup logging
# logger = logging.getLogger(__name__)


# def total_payment(booking_id, conversion_rate):
#     try:
#         booking = get_object_or_404(BookingModel, booking_id=booking_id)
#         if not booking.tour_option:
#             return Decimal("0.00")
#         if booking.tour_option.discount_rate:
#             adult_discount = Decimal(booking.tour_option.discount_rate) / Decimal(100)
#             child_discount = Decimal(booking.tour_option.discount_rate) / Decimal(100)
#             adult_discounted_price = (
#                 Decimal(booking.adults)
#                 * booking.tour_option.adult_retail_price
#                 * (Decimal("1.00") - adult_discount)
#             )
#             if booking.children:
#                 child_discounted_price = (
#                     Decimal(booking.children)
#                     * booking.tour_option.child_retail_price
#                     * (Decimal("1.00") - child_discount)
#                 )
#             else:
#                 child_discounted_price = Decimal("0.00")
#             if booking.infants:
#                 infant_price = Decimal(booking.infants) * Decimal("0.00")
#             else:
#                 infant_price = Decimal("0.00")
#             total_price = (
#                 adult_discounted_price + child_discounted_price + infant_price
#             ) * Decimal(conversion_rate)
#         else:
#             adult_price = (
#                 Decimal(booking.adults) * booking.tour_option.adult_retail_price
#             )
#             if booking.children:
#                 child_price = (
#                     Decimal(booking.children) * booking.tour_option.child_retail_price
#                 )
#             else:
#                 child_price = Decimal("0.00")
#             if booking.infants:
#                 infant_price = Decimal(booking.infants) * Decimal("0.00")
#             else:
#                 infant_price = Decimal("0.00")
#             total_price = (adult_price + child_price + infant_price) * Decimal(
#                 conversion_rate
#             )
#         return total_price.quantize(Decimal("0.01"))
#     except Exception as e:
#         logger.error(
#             f"Error calculating total payment for booking {booking_id}: {str(e)}"
#         )
#         return Decimal("0.00")


# def email_content_en(booking_id):
#     try:
#         booking = get_object_or_404(BookingModel, booking_id=booking_id)
#         formatted_date = booking.tour_date.strftime("%d %B %Y")
#         basarili_mesaj_text = f"""
#             Dear "{booking.full_name}",\n
#             Your booking for the tour "{booking.tour}" has been sent to the operation team succesfully!
#             The general pickup time is {booking.pick_up_time} on {formatted_date}, the operation team will contact you
#             about exact pickup time for the "{booking.hotel_name}".
#             We sent the booking details to your email address, you can download your booking ticket and use it offline.
#             If you need help about more tours, feel free to contact us via whatsapp "+905444733907". \n
#             Have a nice holiday!
#             """
#         return basarili_mesaj_text
#     except Exception as e:
#         logger.error(
#             f"Error generating English email content for booking {booking_id}: {str(e)}"
#         )
#         return "Error generating email content"


# def create_pdf_en(booking_id):
#     try:
#         booking = get_object_or_404(BookingModel, booking_id=booking_id)
#         pdf = FPDF(orientation="P", unit="mm", format="A4")
#         pdf.add_page()

#         # Logo ve Başlık
#         pdf.add_font(
#             family="DejaVuSansMono",
#             style="",
#             fname="static/fonts/DejaVuSansMono.ttf",
#             uni=True,
#         )
#         pdf.set_font("DejaVuSansMono", size=12)
#         pdf.image("static/images/logo-horizontal.png", x=80, y=20, w=50)
#         pdf.ln(40)

#         # Booking Details
#         pdf.set_font("DejaVuSansMono", size=14)
#         pdf.cell(0, 10, "Booking Details", ln=True, align="L")

#         pdf.set_font("DejaVuSansMono", size=12)
#         pdf.cell(
#             0,
#             10,
#             f"Booking Created: {booking.date_created.strftime('%d %B %Y')}",
#             ln=True,
#         )
#         pdf.cell(0, 10, f"Booking ID: {booking.booking_id}", ln=True)
#         pdf.cell(0, 10, f"Tour Name: {booking.tour.tour_title}", ln=True)
#         pdf.cell(0, 10, f"Option Name: {booking.tour_option.title}", ln=True)
#         pdf.cell(
#             0, 10, f"Option Description: {booking.tour_option.description}", ln=True
#         )
#         pdf.cell(0, 10, f"Tour Date: {booking.tour_date.strftime('%d %B %Y')}", ln=True)
#         pdf.cell(0, 10, f"Pickup Time: {booking.pick_up_time}", ln=True)
#         pdf.cell(0, 10, f"Pickup from: {booking.hotel_name}", ln=True)
#         pdf.cell(
#             0,
#             10,
#             f"Total Payment: {booking.total_cost} {booking.selected_curreny}",
#             ln=True,
#         )
#         booking_statu = None
#         if booking.status == "pay_later":
#             booking_statu = "Pay on tour date"
#         elif booking.status == "paid":
#             booking_statu = "All paid"
#         else:
#             booking_statu = "Canceled"

#         pdf.cell(0, 10, f"Payment Status: {booking_statu}", ln=True)
#         pdf.ln(10)

#         # Contact Details
#         pdf.set_font("DejaVuSansMono", size=14)
#         pdf.cell(0, 10, "Contact Details", ln=True, align="L")

#         pdf.set_font("DejaVuSansMono", size=12)
#         pdf.cell(0, 10, f"Full Name: {booking.full_name}", ln=True)
#         pdf.cell(0, 10, f"Email: {booking.email}", ln=True)
#         pdf.cell(0, 10, f"Phone: {booking.phone}", ln=True)
#         pdf.cell(0, 10, f"Adult: {booking.adults}", ln=True)
#         if booking.children:
#             pdf.cell(0, 10, f"Child: {booking.children or 0}", ln=True)
#         if booking.infants:
#             pdf.cell(0, 10, f"Infant: {booking.infants or 0}", ln=True)
#         pdf.cell(0, 10, f"Message: {booking.message or 'No message provided'}", ln=True)
#         pdf.ln(10)

#         # Footer
#         pdf.set_font("DejaVuSansMono", size=12)
#         pdf.set_text_color(100, 100, 100)
#         pdf.multi_cell(
#             0,
#             10,
#             "24/7 contact us via WhatsApp on +905444733907",
#             align="C",
#         )

#         return pdf.output(dest="S")
#     except Exception as e:
#         logger.error(f"Error generating English PDF for booking {booking_id}: {str(e)}")
#         return None


# def email_content_de(booking_id):
#     try:
#         booking = get_object_or_404(BookingModel, booking_id=booking_id)
#         formatted_date = booking.tour_date.strftime("%d %B %Y")
#         basarili_mesaj_text = f"""
#             Sehr geehrte/r "{booking.full_name}",\n
#             Ihre Buchungsanfrage für "{booking.tour}" wurde erfolgreich an unser Operationsteam weitergeleitet!
#             Die allgemeine Abholzeit ist {booking.pick_up_time} am {formatted_date}, aber das Operationsteam wird sich
#             mit Ihnen in Verbindung setzen, um die genaue Abholzeit für Ihr Hotel "{booking.hotel_name}" mitzuteilen.
#             Wir haben die Buchungsdetails an Ihre E-Mail-Adresse gesendet. Sie können Ihr Buchungsticket herunterladen und offline nutzen.
#             Wenn Sie weitere Touren buchen möchten oder Hilfe benötigen, kontaktieren Sie uns gerne über WhatsApp: "+905444733907".\n
#             Wir wünschen Ihnen einen schönen Urlaub!
#             """
#         return basarili_mesaj_text
#     except Exception as e:
#         logger.error(
#             f"Error generating German email content for booking {booking_id}: {str(e)}"
#         )
#         return "Fehler beim Generieren des E-Mail-Inhalts"


# def create_pdf_de(booking_id):
#     try:
#         booking = get_object_or_404(BookingModel, booking_id=booking_id)
#         pdf = FPDF(orientation="P", unit="mm", format="A4")
#         pdf.add_page()

#         # Logo und Titel
#         pdf.add_font(
#             family="DejaVuSansMono",
#             style="",
#             fname="static/fonts/DejaVuSansMono.ttf",
#             uni=True,
#         )
#         pdf.set_font("DejaVuSansMono", size=14)
#         pdf.image("static/images/logo-horizontal.png", x=80, y=20, w=50)
#         pdf.ln(40)

#         # Buchungsdetails
#         pdf.set_font("DejaVuSansMono", size=14)
#         pdf.cell(0, 10, "Buchungsdetails", ln=True, align="L")

#         pdf.set_font("DejaVuSansMono", size=12)
#         pdf.cell(
#             0,
#             10,
#             f"Buchung erstellt: {booking.date_created.strftime('%d %B %Y')}",
#             ln=True,
#         )
#         pdf.cell(0, 10, f"Buchungs-ID: {booking.booking_id}", ln=True)
#         pdf.cell(0, 10, f"Tourname: {booking.tour.tour_title}", ln=True)
#         pdf.cell(0, 10, f"Optionsname: {booking.tour_option.title}_de", ln=True)
#         pdf.cell(
#             0, 10, f"Optionsbeschreibung: {booking.tour_option.description_de}", ln=True
#         )
#         pdf.cell(0, 10, f"Tourdatum: {booking.tour_date.strftime('%d %B %Y')}", ln=True)
#         pdf.cell(0, 10, f"Abholzeit: {booking.pick_up_time}", ln=True)
#         pdf.cell(0, 10, f"Abholung von: {booking.hotel_name}", ln=True)
#         pdf.cell(
#             0,
#             10,
#             f"Gesamtzahlung: {booking.total_cost} {booking.selected_curreny}",
#             ln=True,
#         )
#         booking_status = None
#         if booking.status == "pay_later":
#             booking_status = "Am Tag der Tour bezahlen"
#         elif booking.status == "paid":
#             booking_status = "Vollständig bezahlt"
#         else:
#             booking_status = "Storniert"

#         pdf.cell(0, 10, f"Zahlungsstatus: {booking_status}", ln=True)
#         pdf.ln(10)

#         # Kontaktdetails
#         pdf.set_font("DejaVuSansMono", size=14)
#         pdf.cell(0, 10, "Kontaktdetails", ln=True, align="L")

#         pdf.set_font("DejaVuSansMono", size=12)
#         pdf.cell(0, 10, f"Vollständiger Name: {booking.full_name}", ln=True)
#         pdf.cell(0, 10, f"E-Mail: {booking.email}", ln=True)
#         pdf.cell(0, 10, f"Telefon: {booking.phone}", ln=True)
#         pdf.cell(0, 10, f"Erwachsene: {booking.adults}", ln=True)
#         if booking.children:
#             pdf.cell(0, 10, f"Kinder: {booking.children or 0}", ln=True)
#         if booking.infants:
#             pdf.cell(0, 10, f"Kleinkinder: {booking.infants or 0}", ln=True)
#         pdf.cell(
#             0,
#             10,
#             f"Nachricht: {booking.message or 'Keine Nachricht angegeben'}",
#             ln=True,
#         )
#         pdf.ln(10)

#         # Fußzeile
#         pdf.set_font("DejaVuSansMono", size=12)
#         pdf.set_text_color(100, 100, 100)
#         pdf.multi_cell(
#             0,
#             10,
#             "24/7 WhatsApp unter +905444733907 kontaktieren.",
#             align="C",
#         )

#         return pdf.output(dest="S")
#     except Exception as e:
#         logger.error(f"Error generating German PDF for booking {booking_id}: {str(e)}")
#         return None


# def successfull_email(subject, message, customer_email, content):
#     try:
#         email = EmailMessage(
#             subject=subject,
#             body=message,
#             from_email=settings.BOOKING_EMAIL_SENDER,
#             to=[customer_email],
#             cc=[settings.BOOKING_EMAIL_SENDER],
#         )
#         email.attach(
#             filename="booking_details.pdf",
#             content=content,
#             mimetype="application/pdf",
#         )
#         email.content_subtype = "html"
#         email.send()
#         return True
#     except Exception as e:
#         logger.error(f"Error sending email to {customer_email}: {str(e)}")
#         return False
