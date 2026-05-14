# WORKFLOW 
def apply_workflow_rules(
    extracted_data: dict
):

    invoice_total = extracted_data.get(
        "invoice_total"
    )

    # NO TOTAL FOUND
    if not invoice_total:

        return {
            "status": "rejected",
            "reason": "Invoice total not found."
        }

    # =========================
    # HANDLE DICTIONARY FORMAT
    # =========================
    if isinstance(invoice_total, dict):

        amount = invoice_total.get(
            "amount"
        )

    else:

        try:

            amount = float(
                str(invoice_total)
                .replace("$", "")
                .replace(",", "")
            )

        except Exception:

            return {
                "status": "pending_review",
                "reason": "Could not process invoice amount."
            }

    # =========================
    # INVALID AMOUNT
    # =========================
    if amount is None:

        return {
            "status": "pending_review",
            "reason": "Invoice amount is invalid."
        }

    # =========================
    # BUSINESS RULES
    # =========================
    if amount < 1000:

        return {
            "status": "approved",
            "reason": "Invoice amount below approval threshold."
        }

    elif amount >= 1000:

        return {
            "status": "pending_review",
            "reason": "Invoice requires manual review."
        }

    # =========================
    # DEFAULT
    # =========================
    return {
        "status": "pending_review",
        "reason": "Workflow could not determine status."
    }