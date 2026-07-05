import re
from typing import Optional


# ----------------------------------------------------------------------
# Device detection patterns (order matters)
# ----------------------------------------------------------------------
_DEVICE_PATTERNS = [
    (re.compile(r"\biPad\b", re.IGNORECASE), "tablet"),
    (re.compile(r"\bAndroid\b(?:[^;]*;)?(?:?!Mobile)", re.IGNORECASE), "tablet"),
    (re.compile(r"\b(Mobile|Android|iPhone|iphone|Windows Phone|IEMobile|Opera Mobi)\b", re.IGNORECASE), "mobile"),
]

# ----------------------------------------------------------------------
# Browser detection patterns (order matters — specificity first)
# ----------------------------------------------------------------------
_BROWSER_PATTERNS = [
    (re.compile(r"\b(Edg|Edge)/(\d+)", re.IGNORECASE), "Edge"),
    (re.compile(r"\bOPR/(\d+)", re.IGNORECASE), "Opera"),
    (re.compile(r"\bChrome/(\d+).*?\(?.*?(?!Chromium).*\b(?:Firefox|OPR)", re.IGNORECASE), "Firefox"),
    (re.compile(r"\bFirefox/(\d+)", re.IGNORECASE), "Firefox"),
    (re.compile(r"\bSamsungBrowser/(\d+)", re.IGNORECASE), "Samsung Browser"),
    (re.compile(r"\bUC?Browser/(\d+)", re.IGNORECASE), "UC Browser"),
    (re.compile(r"\bCriOS/(\d+)", re.IGNORECASE), "Chrome iOS"),
    (re.compile(r"\bFxiOS/(\d+)", re.IGNORECASE), "Firefox iOS"),
    (re.compile(r"\bChrome/(\d+)", re.IGNORECASE), "Chrome"),
    (re.compile(r"\bSafari/(\d+)", re.IGNORECASE), "Safari"),
    (re.compile(r"\bMSIE (\d+)", re.IGNORECASE), "IE"),
    (re.compile(r"\bTrident/.*?; rv:(\d+)", re.IGNORECASE), "IE"),
]

# ----------------------------------------------------------------------
# OS detection patterns (order matters)
# ----------------------------------------------------------------------
_OS_PATTERNS = [
    (re.compile(r"\biPhone.*?OS (\d+)", re.IGNORECASE), "iOS"),
    (re.compile(r"\biPad.*?OS (\d+)", re.IGNORECASE), "iPadOS"),
    (re.compile(r"\bAndroid (\d+[\.\d]*)", re.IGNORECASE), "Android"),
    (re.compile(r"\bWindows NT 10\.0\b", re.IGNORECASE), "Windows 10/11"),
    (re.compile(r"\bWindows NT 6\.3\b", re.IGNORECASE), "Windows 8.1"),
    (re.compile(r"\bWindows NT 6\.2\b", re.IGNORECASE), "Windows 8"),
    (re.compile(r"\bWindows NT 6\.1\b", re.IGNORECASE), "Windows 7"),
    (re.compile(r"\bWindows NT\b", re.IGNORECASE), "Windows"),
    (re.compile(r"\bMac OS X (\d+[\.\d]*)", re.IGNORECASE), "macOS"),
    (re.compile(r"\bMacintosh\b", re.IGNORECASE), "macOS"),
    (re.compile(r"\bLinux\b", re.IGNORECASE), "Linux"),
    (re.compile(r"\bCrOS\b", re.IGNORECASE), "Chrome OS"),
]


def parse_user_agent(user_agent: str) -> dict:
    """
    Parse a User-Agent string and return a dict with:
      - device_type: desktop | mobile | tablet | unknown
      - browser:      string | None
      - os:           string | None
    """
    if not user_agent:
        return {"device_type": "unknown", "browser": None, "os": None}

    device_type = "desktop"
    browser = None
    os_name = None

    # Device type
    for pattern, dtype in _DEVICE_PATTERNS:
        if pattern.search(user_agent):
            device_type = dtype
            break

    # Browser (first match wins)
    for pattern, bname in _BROWSER_PATTERNS:
        if pattern.search(user_agent):
            browser = bname
            break

    # OS (first match wins)
    for pattern, oname in _OS_PATTERNS:
        if pattern.search(user_agent):
            os_name = oname
            break

    return {
        "device_type": device_type,
        "browser": browser,
        "os": os_name,
    }


def get_client_ip(request) -> Optional[str]:
    """
    Extract the real client IP from a Django request object.
    Handles X-Forwarded-For (when behind a proxy/load balancer) and
    X-Real-IP headers, falling back to META REMOTE_ADDR.
    """
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded:
        # First IP in the list is the original client
        ip = x_forwarded.split(",")[0].strip()
        return ip
    x_real = request.META.get("HTTP_X_REAL_IP")
    if x_real:
        return x_real.strip()
    return request.META.get("REMOTE_ADDR")


def extract_utm(query_params: dict) -> dict:
    """
    Extract UTM parameters from a Django request GET/POST QueryDict.
    Returns a dict with keys: utm_source, utm_medium, utm_campaign.
    Safe to call with any query dict (handles missing keys gracefully).
    """
    def get(key: str) -> Optional[str]:
        val = query_params.get(key)
        if val and isinstance(val, str):
            val = val.strip()
            return val if val else None
        return None

    return {
        "utm_source": get("utm_source"),
        "utm_medium": get("utm_medium"),
        "utm_campaign": get("utm_campaign"),
    }
