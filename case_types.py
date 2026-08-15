import random

CASE_TYPES = [
    # Contracts and business
    "contract dispute",
    "breach of contract",
    "business partnership dispute",
    "shareholder dispute",
    "business acquisition dispute",
    "supplier dispute",
    "service agreement dispute",
    "non-compete agreement dispute",
    "franchise dispute",
    "commission dispute",
    "debt or payment dispute",
    "loan agreement dispute",

    # Employment
    "wrongful termination dispute",
    "workplace discrimination dispute",
    "workplace harassment dispute",
    "unpaid wages dispute",
    "overtime pay dispute",
    "employee commission dispute",
    "employment contract dispute",
    "employee confidentiality dispute",
    "workplace retaliation dispute",
    "employee classification dispute",

    # Property and housing
    "landlord-tenant dispute",
    "security deposit dispute",
    "eviction dispute",
    "lease violation dispute",
    "property boundary dispute",
    "easement dispute",
    "property ownership dispute",
    "property damage dispute",
    "home sale dispute",
    "real estate disclosure dispute",
    "zoning dispute",
    "construction defect dispute",
    "neighbor nuisance dispute",
    "tree or vegetation property dispute",

    # Personal injury and negligence
    "car accident dispute",
    "pedestrian accident dispute",
    "bicycle accident dispute",
    "slip-and-fall dispute",
    "premises liability dispute",
    "negligent maintenance dispute",
    "product injury dispute",
    "professional negligence dispute",
    "general negligence dispute",
    "animal injury dispute",
    "sports injury dispute",
    "public transportation injury dispute",

    # Consumer
    "defective product dispute",
    "consumer warranty dispute",
    "online purchase dispute",
    "subscription service dispute",
    "automobile purchase dispute",
    "home repair dispute",
    "travel service dispute",
    "hotel service dispute",
    "refund dispute",
    "advertising dispute",

    # Insurance
    "insurance claim dispute",
    "property insurance dispute",
    "vehicle insurance dispute",
    "health insurance coverage dispute",
    "life insurance beneficiary dispute",
    "business interruption insurance dispute",

    # Professional services
    "lawyer-client fee dispute",
    "accountant-client dispute",
    "architect-client dispute",
    "consultant-client dispute",
    "contractor-client dispute",
    "real estate agent dispute",
    "financial advisor dispute",

    # Intellectual property and media
    "copyright dispute",
    "trademark dispute",
    "trade secret dispute",
    "software licensing dispute",
    "photography rights dispute",
    "publication rights dispute",
    "defamation dispute",
    "online defamation dispute",

    # Family and inheritance
    "inheritance dispute",
    "will interpretation dispute",
    "estate administration dispute",
    "trust dispute",
    "family property dispute",

    # Finance
    "banking dispute",
    "credit agreement dispute",
    "credit reporting dispute",
    "investment dispute",
    "financial transaction dispute",
    "fraud-related civil dispute",

    # Technology
    "software development dispute",
    "data ownership dispute",
    "website development dispute",
    "technology service agreement dispute",
    "digital content dispute",
    "online platform dispute",

    # Other civil disputes
    "privacy dispute",
    "licensing dispute",
    "permit dispute",
    "environmental damage dispute",
    "noise nuisance dispute",
    "business reputation dispute",
    "public accommodation dispute",
    "event cancellation dispute",
    "storage facility dispute",
    "parking dispute",
    "lost property dispute",
    "auction dispute",
    "delivery dispute",
    "shipping damage dispute",
]

def get_random_case_type():
    return random.choice(CASE_TYPES)