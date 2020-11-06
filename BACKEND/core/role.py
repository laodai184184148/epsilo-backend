
from pydantic import  BaseSettings
from urllib.parse import quote_plus


class Scope(BaseSettings):

    SCOPES={
        "READ_USER":"VIEW ALL USER AND USER DETAIL",
        "READ_SHOP":"VIEW ALL SHOP AND SHOP DETAIL",
        "READ_CHANNEL":"VIEW ALL CHANNEL AND CHANNEL DETAIL",
        "READ_COUNTRY":"VIEW ALL COUNTRY AND COUNTRY DETAIL",
        "READ_SIM":"VIEW ALL SIM DETAILS",
        "TAG":"SIM TAGGING FUNCTION",
        "INACTIVATE_USER":"IN ACTIVATE USER",
        "URL":"URL FUNCTION"
        }
    EXECUTOR_SCOPESS=[
        "ME",
        "READ_USER",
        "READ_SHOP",
        "READ_CHANNEL",
        "READ_COUNTRY",
        "READ_SIM"
        ]
    MANAGER_SCOPESS=[
        "ME",
        "READ_USER",
        "READ_SHOP",
        "READ_CHANNEL",
        "READ_COUNTRY",
        "READ_SIM"
    ]
    ADMIN_SCOPESS=[
        "ME",
        "READ_USER",
        "READ_SHOP",
        "READ_CHANNEL",
        "READ_COUNTRY",
        "READ_SIM",
        "INACTIVATE_USER",
        "URL",
        "TAG"
    ]

    class Config:
        case_sensitive = True
scope = Scope()