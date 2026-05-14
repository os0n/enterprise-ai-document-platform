from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from app.config.settings import (
    AZURE_ENDPOINT,
    AZURE_KEY
)


def analyze_invoice(
    file_bytes: bytes
) -> dict:

    try:

        client = DocumentAnalysisClient(
            endpoint=AZURE_ENDPOINT,
            credential=AzureKeyCredential(
                AZURE_KEY
            )
        )

        poller = client.begin_analyze_document(
            "prebuilt-invoice",
            document=file_bytes
        )

        result = poller.result()

        extracted_data = {}

        for invoice in result.documents:

            fields = invoice.fields

            def get_field_value(
                field_name
            ):

                field = fields.get(
                    field_name
                )

                if field is None:
                    return None

                try:
                    return field.value

                except Exception:
                    return None

            extracted_data = {

                "vendor_name": get_field_value(
                    "VendorName"
                ),

                "vendor_address": get_field_value(
                    "VendorAddress"
                ),

                "customer_name": get_field_value(
                    "CustomerName"
                ),

                "invoice_id": get_field_value(
                    "InvoiceId"
                ),

                "invoice_date": str(
                    get_field_value(
                        "InvoiceDate"
                    )
                ),

                "due_date": str(
                    get_field_value(
                        "DueDate"
                    )
                ),

                "invoice_total": get_field_value(
                    "InvoiceTotal"
                ),

                "subtotal": get_field_value(
                    "SubTotal"
                ),

                "tax": get_field_value(
                    "TotalTax"
                ),
            }

        return extracted_data

    except Exception as e:

        return {
            "error": str(e)
        }