from typing import Any


PRODUCT_RULES = {
    "platinum wealth": {
        "product_name": "Platinum Wealth Account",
         "priority": 3,
        "min_age": 25,
        "max_age": 60,
        "min_annual_income": 1_500_000,
        "required_kyc_status": "ACTIVE",
        "allowed_risk_segments": ["LOW", "MEDIUM"],
    },
    "premium savings": {
        "product_name": "Premium Savings Account",
        "priority": 2,
        "min_age": 21,
        "max_age": None,
        "min_annual_income": 800_000,
        "required_kyc_status": "ACTIVE",
        "allowed_risk_segments": None,
    },
    "classic savings": {
        "product_name": "Classic Savings Account",
        "priority": 1,
        "min_age": 18,
        "max_age": None,
        "min_annual_income": None,
        "required_kyc_status": "ACTIVE",
        "allowed_risk_segments": None,
    },
}


def check_eligibility(
    customer: dict[str, Any],
    product_name: str,
) -> dict:
    """
    Deterministically check whether a customer satisfies the eligibility
    rules for a bank product.

    Use this tool only after customer information has been retrieved.

    Args:
        customer: Customer profile containing age, annual_income,
            kyc_status and risk_segment.
        product_name: Product name such as "Platinum Wealth".

    Returns:
        Eligibility decision with passed and failed criteria.
    """

    product_key = product_name.strip().lower()

    rules = PRODUCT_RULES.get(product_key)

    if not rules:
        return {
            "status": "product_not_found",
            "eligible": False,
            "message": f"No deterministic eligibility rules found for {product_name}.",
        }

    passed = []
    failed = []

    age = customer.get("age")

    if age is None:
        failed.append("Customer age is unavailable.")
    else:
        if age < rules["min_age"]:
            failed.append(
                f"Age {age} is below minimum age {rules['min_age']}."
            )
        elif (
            rules["max_age"] is not None
            and age > rules["max_age"]
        ):
            failed.append(
                f"Age {age} exceeds maximum age {rules['max_age']}."
            )
        else:
            passed.append("Age requirement satisfied.")

    income = customer.get("annual_income")

    if rules["min_annual_income"] is not None:
        if income is None:
            failed.append("Annual income is unavailable.")
        elif income < rules["min_annual_income"]:
            failed.append(
                f"Annual income INR {income:,} is below required "
                f"INR {rules['min_annual_income']:,}."
            )
        else:
            passed.append("Annual income requirement satisfied.")

    kyc_status = customer.get("kyc_status")

    if kyc_status != rules["required_kyc_status"]:
        failed.append(
            f"KYC status must be {rules['required_kyc_status']}."
        )
    else:
        passed.append("KYC requirement satisfied.")

    allowed_risk_segments = rules["allowed_risk_segments"]

    if allowed_risk_segments is not None:
        risk_segment = customer.get("risk_segment")

        if risk_segment not in allowed_risk_segments:
            failed.append(
                f"Risk segment must be one of {allowed_risk_segments}."
            )
        else:
            passed.append("Risk segment requirement satisfied.")

    eligible = len(failed) == 0

    return {
        "status": "success",
        "product": rules["product_name"],
        "eligible": eligible,
        "passed_criteria": passed,
        "failed_criteria": failed,
    }
    
    
def find_eligible_alternatives(
    customer: dict,
    exclude_product: str,
) -> dict:
    """
    Find alternative products for which the customer is eligible.

    Args:
        customer: Customer profile.
        exclude_product: Product to exclude from the alternatives.

    Returns:
        Eligible alternative products.
    """

    alternatives = []

    excluded_key = exclude_product.strip().lower()

    for product_key, rules in PRODUCT_RULES.items():
        if product_key == excluded_key:
            continue

        result = check_eligibility(
            customer=customer,
            product_name=product_key,
        )

        if result.get("eligible"):
            alternatives.append(
                {
                    "product": result["product"],
                    "priority": rules["priority"],
                    "passed_criteria": result["passed_criteria"],
                }
            )

    alternatives.sort(
        key=lambda x: x["priority"],
        reverse=True,
    )
    
    return {
        "status": "success",
        "recommended_product": (
            alternatives[0]["product"] if alternatives else None
        ),
        "alternatives": alternatives,
    }