"""Urgent server-side confinement: no network, browser or deferred worker."""
from .models import RefonteAudit

MANUAL_MESSAGE = "Analyse automatique désactivée. Votre demande est enregistrée pour une prise en charge manuelle."

class AutomaticAnalysisDisabled(RuntimeError):
    pass

def analyze_site(url):
    return {"status": "non_analysable", "reason": MANUAL_MESSAGE}

def analyze_site_with_playwright(url):
    return analyze_site(url)

def check_resources(base_url, resources):
    return []

def fetch_pagespeed(url):
    return {"status": "unavailable", "reason": MANUAL_MESSAGE}

def build_heuristics(technical, pagespeed):
    return []

def _request(*args, **kwargs):
    raise AutomaticAnalysisDisabled(MANUAL_MESSAGE)

def run_refonte_analysis(audit_id):
    RefonteAudit.objects.filter(pk=audit_id).update(
        analysis_status=RefonteAudit.AnalysisStatus.NON_ANALYSABLE,
        technical_report=analyze_site(None), pagespeed_report=fetch_pagespeed(None),
        heuristic_report=[], analysis_error=MANUAL_MESSAGE,
    )

def schedule_refonte_analysis(audit_id):
    # Synchronous local update; no on_commit task/thread survives the boundary.
    run_refonte_analysis(audit_id)
