from services.data_fetcher import account_service, contact_service, project_service
def fetch_account_data():
    return account_service()

def fetch_contact_data():
    return contact_service()

def fetch_project_data():
    return project_service()