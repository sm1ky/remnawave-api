from datetime import datetime
from typing import Dict, Type

import httpx

from remnawave.enums import ErrorCode
from .general import (
    ApiError,
    ApiErrorResponse,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    ServerError,
    UnauthorizedError,
    ValidationError,
    NetworkError,
    AuthenticationError,
    BusinessLogicError,
)

ERRORS: Dict[str, Type[ApiError]] = {
    ErrorCode.INTERNAL_SERVER_ERROR: ServerError,
    ErrorCode.LOGIN_ERROR: AuthenticationError,
    ErrorCode.UNAUTHORIZED: UnauthorizedError,
    ErrorCode.FORBIDDEN_ROLE_ERROR: ForbiddenError,
    ErrorCode.CREATE_API_TOKEN_ERROR: ServerError,
    ErrorCode.DELETE_API_TOKEN_ERROR: ServerError,
    ErrorCode.REQUESTED_TOKEN_NOT_FOUND: NotFoundError,
    ErrorCode.FIND_ALL_API_TOKENS_ERROR: ServerError,
    ErrorCode.GET_PUBLIC_KEY_ERROR: ServerError,
    ErrorCode.ENABLE_NODE_ERROR: ServerError,
    ErrorCode.NODE_NOT_FOUND: NotFoundError,
    ErrorCode.CONFIG_NOT_FOUND: NotFoundError,
    ErrorCode.UPDATE_CONFIG_ERROR: ServerError,
    ErrorCode.GET_CONFIG_ERROR: ServerError,
    ErrorCode.DELETE_MANY_INBOUNDS_ERROR: ServerError,
    ErrorCode.CREATE_MANY_INBOUNDS_ERROR: ServerError,
    ErrorCode.FIND_ALL_INBOUNDS_ERROR: ServerError,
    ErrorCode.CREATE_USER_ERROR: ServerError,
    ErrorCode.USER_USERNAME_ALREADY_EXISTS: ConflictError,
    ErrorCode.USER_SHORT_UUID_ALREADY_EXISTS: ConflictError,
    ErrorCode.USER_SUBSCRIPTION_UUID_ALREADY_EXISTS: ConflictError,
    ErrorCode.CREATE_USER_WITH_INBOUNDS_ERROR: ServerError,
    ErrorCode.CANT_GET_CREATED_USER_WITH_INBOUNDS: ServerError,
    ErrorCode.GET_ALL_USERS_ERROR: ServerError,
    ErrorCode.USER_NOT_FOUND: NotFoundError,
    ErrorCode.GET_USER_BY_ERROR: ServerError,
    ErrorCode.REVOKE_USER_SUBSCRIPTION_ERROR: ServerError,
    ErrorCode.DISABLE_USER_ERROR: ServerError,
    ErrorCode.USER_ALREADY_DISABLED: ConflictError,
    ErrorCode.USER_ALREADY_ENABLED: ConflictError,
    ErrorCode.ENABLE_USER_ERROR: ServerError,
    ErrorCode.CREATE_NODE_ERROR: ServerError,
    ErrorCode.NODE_NAME_ALREADY_EXISTS: ConflictError,
    ErrorCode.NODE_ADDRESS_ALREADY_EXISTS: ConflictError,
    ErrorCode.NODE_ERROR_WITH_MSG: ServerError,
    ErrorCode.NODE_ERROR_500_WITH_MSG: ServerError,
    ErrorCode.RESTART_NODE_ERROR: ServerError,
    ErrorCode.GET_CONFIG_WITH_USERS_ERROR: ServerError,
    ErrorCode.DELETE_USER_ERROR: ServerError,
    ErrorCode.UPDATE_NODE_ERROR: ServerError,
    ErrorCode.UPDATE_USER_ERROR: ServerError,
    ErrorCode.INCREMENT_USED_TRAFFIC_ERROR: ServerError,
    ErrorCode.GET_ALL_NODES_ERROR: ServerError,
    ErrorCode.GET_ONE_NODE_ERROR: ServerError,
    ErrorCode.DELETE_NODE_ERROR: ServerError,
    ErrorCode.CREATE_HOST_ERROR: ServerError,
    ErrorCode.HOST_REMARK_ALREADY_EXISTS: ConflictError,
    ErrorCode.HOST_NOT_FOUND: NotFoundError,
    ErrorCode.DELETE_HOST_ERROR: ServerError,
    ErrorCode.GET_USER_STATS_ERROR: ServerError,
    ErrorCode.UPDATE_USER_WITH_INBOUNDS_ERROR: ServerError,
    ErrorCode.GET_ALL_HOSTS_ERROR: ServerError,
    ErrorCode.REORDER_HOSTS_ERROR: ServerError,
    ErrorCode.UPDATE_HOST_ERROR: ServerError,
    ErrorCode.CREATE_CONFIG_ERROR: ServerError,
    ErrorCode.ENABLED_NODES_NOT_FOUND: ConflictError,
    ErrorCode.GET_NODES_USAGE_BY_RANGE_ERROR: ServerError,
    ErrorCode.RESET_USER_TRAFFIC_ERROR: ServerError,
    ErrorCode.REORDER_NODES_ERROR: ServerError,
    ErrorCode.GET_ALL_INBOUNDS_ERROR: ServerError,
    ErrorCode.BULK_DELETE_USERS_BY_STATUS_ERROR: ServerError,
    ErrorCode.UPDATE_INBOUND_ERROR: ServerError,
    ErrorCode.CONFIG_VALIDATION_ERROR: ValidationError,
    ErrorCode.USERS_NOT_FOUND: NotFoundError,
    ErrorCode.GET_USER_BY_UNIQUE_FIELDS_NOT_FOUND: NotFoundError,
    ErrorCode.UPDATE_EXCEEDED_TRAFFIC_USERS_ERROR: ServerError,
    ErrorCode.ADMIN_NOT_FOUND: NotFoundError,
    ErrorCode.CREATE_ADMIN_ERROR: ServerError,
    ErrorCode.GET_AUTH_STATUS_ERROR: ServerError,
    ErrorCode.FORBIDDEN_ONE: ForbiddenError,
    ErrorCode.FORBIDDEN_TWO: ForbiddenError,
    ErrorCode.DISABLE_NODE_ERROR: ServerError,
    ErrorCode.GET_ONE_HOST_ERROR: ServerError,
    ErrorCode.SUBSCRIPTION_SETTINGS_NOT_FOUND: NotFoundError,
    ErrorCode.GET_SUBSCRIPTION_SETTINGS_ERROR: ServerError,
    ErrorCode.UPDATE_SUBSCRIPTION_SETTINGS_ERROR: ServerError,
    
    ErrorCode.CREATE_SUBSCRIPTION_TEMPLATE_ERROR: ServerError,
    ErrorCode.SUBSCRIPTION_TEMPLATE_NOT_FOUND: NotFoundError,
    ErrorCode.UPDATE_SUBSCRIPTION_TEMPLATE_ERROR: ServerError,
    ErrorCode.DELETE_SUBSCRIPTION_TEMPLATE_ERROR: ServerError,
    ErrorCode.GET_SUBSCRIPTION_TEMPLATE_ERROR: ServerError,
    
    ErrorCode.CREATE_INBOUND_ERROR: ServerError,
    ErrorCode.DELETE_INBOUND_ERROR: ServerError,
    ErrorCode.GET_INBOUND_ERROR: ServerError,
    ErrorCode.INBOUND_NOT_FOUND: NotFoundError,
    ErrorCode.INBOUND_TAG_ALREADY_EXISTS: ConflictError,
    
    ErrorCode.CREATE_EXTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.EXTERNAL_SQUAD_NOT_FOUND: NotFoundError,
    ErrorCode.UPDATE_EXTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.DELETE_EXTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.EXTERNAL_SQUAD_NAME_ALREADY_EXISTS: ConflictError,
    ErrorCode.ADD_USERS_TO_EXTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.REMOVE_USERS_FROM_EXTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.GET_EXTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.GET_ALL_EXTERNAL_SQUADS_ERROR: ServerError,
    
    ErrorCode.CREATE_INTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.INTERNAL_SQUAD_NOT_FOUND: NotFoundError,
    ErrorCode.UPDATE_INTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.DELETE_INTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.INTERNAL_SQUAD_NAME_ALREADY_EXISTS: ConflictError,
    ErrorCode.GET_INTERNAL_SQUAD_ERROR: ServerError,
    ErrorCode.GET_ALL_INTERNAL_SQUADS_ERROR: ServerError,
    
    ErrorCode.CREATE_SNIPPET_ERROR: ServerError,
    ErrorCode.SNIPPET_NOT_FOUND: NotFoundError,
    ErrorCode.UPDATE_SNIPPET_ERROR: ServerError,
    ErrorCode.DELETE_SNIPPET_ERROR: ServerError,
    ErrorCode.SNIPPET_NAME_ALREADY_EXISTS: ConflictError,
    ErrorCode.GET_SNIPPET_ERROR: ServerError,
    ErrorCode.GET_ALL_SNIPPETS_ERROR: ServerError,
    
    # Валидационные ошибки
    ErrorCode.VALIDATION_ERROR: ValidationError,
    ErrorCode.INVALID_UUID_FORMAT: ValidationError,
    ErrorCode.INVALID_EMAIL_FORMAT: ValidationError,
    ErrorCode.INVALID_DATE_FORMAT: ValidationError,
    ErrorCode.REQUIRED_FIELD_MISSING: ValidationError,
    ErrorCode.FIELD_TOO_LONG: ValidationError,
    ErrorCode.FIELD_TOO_SHORT: ValidationError,
    ErrorCode.INVALID_ENUM_VALUE: ValidationError,
    ErrorCode.INVALID_REGEX_PATTERN: ValidationError,
    ErrorCode.NUMERIC_VALIDATION_ERROR: ValidationError,
    
    # Сетевые ошибки
    ErrorCode.NETWORK_ERROR: NetworkError,
    ErrorCode.TIMEOUT_ERROR: NetworkError,
    ErrorCode.CONNECTION_ERROR: NetworkError,
    ErrorCode.DNS_ERROR: NetworkError,
    ErrorCode.SSL_ERROR: NetworkError,
    
    # Ошибки аутентификации
    ErrorCode.INVALID_TOKEN: AuthenticationError,
    ErrorCode.TOKEN_EXPIRED: AuthenticationError,
    ErrorCode.INVALID_CREDENTIALS: AuthenticationError,
    ErrorCode.TWO_FACTOR_REQUIRED: AuthenticationError,
    ErrorCode.ACCOUNT_LOCKED: AuthenticationError,
    ErrorCode.PASSWORD_COMPLEXITY_ERROR: ValidationError,
    
    # Бизнес-логика
    ErrorCode.TRAFFIC_LIMIT_EXCEEDED: BusinessLogicError,
    ErrorCode.USER_LIMIT_EXCEEDED: BusinessLogicError,
    ErrorCode.SUBSCRIPTION_EXPIRED: BusinessLogicError,
    ErrorCode.FEATURE_NOT_AVAILABLE: BusinessLogicError,
    ErrorCode.QUOTA_EXCEEDED: BusinessLogicError,
    ErrorCode.RESOURCE_LOCKED: ConflictError,
    
    # Системные ошибки
    ErrorCode.SYSTEM_STATS_ERROR: ServerError,
    ErrorCode.SYSTEM_HEALTH_ERROR: ServerError,
    ErrorCode.NODES_METRICS_ERROR: ServerError,
    ErrorCode.X25519_KEYGEN_ERROR: ServerError,
    ErrorCode.HAPP_CRYPTO_ERROR: ServerError,
    ErrorCode.SRR_MATCHER_ERROR: ServerError,
    
    # Настройки Remnawave
    ErrorCode.GET_REMNAWAVE_SETTINGS_ERROR: ServerError,
    ErrorCode.UPDATE_REMNAWAVE_SETTINGS_ERROR: ServerError,
    ErrorCode.OAUTH_ERROR: AuthenticationError,
    ErrorCode.PASSKEY_SETTINGS_ERROR: ServerError,
    ErrorCode.TELEGRAM_AUTH_ERROR: AuthenticationError,
    ErrorCode.BRANDING_SETTINGS_ERROR: ServerError,
}


# ---------------------------------------------------------------------------
# Panel error codes, taken from the error DTOs of the Remnawave OpenAPI document
# (openapi/remna-3-4-3.json).
#
# Keyed by the raw code the panel sends rather than by ``ErrorCode`` member: a
# number of members still carry values assigned by much older API versions, so
# their names cannot be trusted to select the right exception. Applied after the
# table above, which keeps the codes the panel no longer documents.
#
# A089, A219 are deliberately left out — the panel reuses each of them for
# two unrelated errors, so the HTTP status is the only reliable signal.
# ---------------------------------------------------------------------------
_CONFLICT_CODES = (
    "A019", "A020", "A021", "A033", "A034", "A045", "A098", "A164", "A176", "A189", "A210",
    "A223", "A244", "A246"
)

_BAD_REQUEST_CODES = (
    "A029", "A030", "A099", "A144", "A145", "A149", "A152", "A153", "A166", "A167", "A172",
    "A173", "A174", "A175", "A178", "A180", "A190", "A194", "A195", "A209", "A212", "A215",
    "A216", "A229", "A230", "A235"
)

_NOT_FOUND_CODES = (
    "A007", "A011", "A012", "A025", "A046", "A062", "A063", "A065", "A071", "A076", "A111",
    "A118", "A124", "A128", "A147", "A162", "A170", "A182", "A191", "A204", "A206", "A218",
    "A220", "A226", "A238", "A245"
)

_SERVER_ERROR_CODES = (
    "A001", "A002", "A005", "A006", "A008", "A009", "A010", "A013", "A014", "A015", "A016",
    "A017", "A018", "A022", "A023", "A024", "A026", "A027", "A028", "A031", "A032", "A035",
    "A036", "A037", "A038", "A039", "A040", "A041", "A042", "A043", "A044", "A047", "A048",
    "A049", "A050", "A051", "A052", "A053", "A055", "A056", "A057", "A058", "A059", "A060",
    "A064", "A066", "A067", "A069", "A070", "A072", "A073", "A074", "A075", "A077", "A078",
    "A079", "A080", "A081", "A084", "A085", "A086", "A087", "A088", "A090", "A091", "A092",
    "A093", "A096", "A097", "A100", "A101", "A102", "A103", "A104", "A105", "A106", "A107",
    "A108", "A109", "A110", "A112", "A115", "A116", "A117", "A119", "A121", "A122", "A123",
    "A125", "A126", "A127", "A129", "A130", "A131", "A132", "A133", "A134", "A135", "A136",
    "A137", "A138", "A139", "A140", "A141", "A142", "A143", "A146", "A148", "A150", "A151",
    "A154", "A155", "A156", "A157", "A158", "A159", "A160", "A161", "A163", "A165", "A168",
    "A169", "A171", "A177", "A179", "A181", "A183", "A184", "A185", "A186", "A187", "A188",
    "A192", "A193", "A196", "A197", "A198", "A199", "A200", "A201", "A202", "A203", "A205",
    "A207", "A208", "A211", "A213", "A214", "A217", "A221", "A224", "A225", "A227", "A228",
    "A232", "A233", "A234", "A236", "A237", "A239", "A240", "A241", "A242", "A243", "A247",
    "A248", "A249", "A250", "A251", "A254", "A256", "A257"
)

for _codes, _exception in (
    (_CONFLICT_CODES, ConflictError),
    (_BAD_REQUEST_CODES, BadRequestError),
    (_NOT_FOUND_CODES, NotFoundError),
    (_SERVER_ERROR_CODES, ServerError),
):
    ERRORS.update(dict.fromkeys(_codes, _exception))


def handle_api_error(response: httpx.Response) -> None:
    """Handle API error responses and raise appropriate exceptions"""
    if response.status_code >= 400:
        try:
            error_data = response.json()
            error_response = ApiErrorResponse(**error_data)
            
            # Fill missing fields for API v2 format
            if error_response.timestamp is None:
                error_response.timestamp = datetime.now()
            if error_response.path is None:
                error_response.path = str(response.request.url.path)
            if error_response.code is None:
                # Use status_code or default to UNKNOWN
                if error_response.status_code:
                    error_response.code = f"HTTP_{error_response.status_code}"
                else:
                    error_response.code = "UNKNOWN"

            # Map error code to exception class
            if error_response.code in ERRORS:
                exception_class = ERRORS[error_response.code]
            else:
                # Fallback based on HTTP status code
                exception_class = _get_exception_by_status_code(response.status_code)

            raise exception_class(response.status_code, error_response)
            
        except ValueError:
            # JSON parsing failed, create generic error
            raise ApiError(
                response.status_code,
                ApiErrorResponse(
                    timestamp=datetime.now(),
                    path=str(response.request.url.path),
                    message=f"Unknown error: {response.text}",
                    code="UNKNOWN",
                    status_code=response.status_code,
                ),
            )


def _get_exception_by_status_code(status_code: int) -> Type[ApiError]:
    """Get exception class based on HTTP status code"""
    if status_code == 400:
        return BadRequestError
    elif status_code == 401:
        return UnauthorizedError
    elif status_code == 403:
        return ForbiddenError
    elif status_code == 404:
        return NotFoundError
    elif status_code == 409:
        return ConflictError
    elif status_code == 422:
        return ValidationError
    elif status_code == 429:
        return BadRequestError  # Rate limit
    elif status_code >= 500:
        return ServerError
    else:
        return ApiError