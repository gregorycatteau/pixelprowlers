from __future__ import annotations

import json
import os
import ssl
import time
from html.parser import HTMLParser
from threading import Thread
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse, urlencode
from urllib.request import Request, urlopen

from django.db import close_old_connections, transaction

from .models import RefonteAudit


REQUEST_TIMEOUT_SECONDS = 15
SLOW_RESOURCE_SECONDS = 2


class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta: dict[str, str] = {}
        self.resources: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key.lower(): value or "" for key, value in attrs}

        if tag == "title":
            self._in_title = True

        if tag == "meta":
            key = attr_map.get("name") or attr_map.get("property")
            content = attr_map.get("content", "")
            if key and content:
                self.meta[key.lower()] = content.strip()

        if tag in {"script", "img", "iframe"} and attr_map.get("src"):
            self.resources.append(attr_map["src"])

        if tag == "link" and attr_map.get("href") and attr_map.get("rel") in {"stylesheet", "preload", "modulepreload"}:
            self.resources.append(attr_map["href"])

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data.strip()

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False


def schedule_refonte_analysis(audit_id: int) -> None:
    transaction.on_commit(lambda: Thread(target=run_refonte_analysis, args=(audit_id,), daemon=True).start())


def run_refonte_analysis(audit_id: int) -> None:
    close_old_connections()
    try:
        audit = RefonteAudit.objects.get(pk=audit_id)
    except RefonteAudit.DoesNotExist:
        close_old_connections()
        return

    try:
        technical_report = analyze_site(audit.site_url)
        pagespeed_report = fetch_pagespeed(audit.site_url)
        heuristic_report = build_heuristics(technical_report, pagespeed_report)

        if technical_report["status"] == "non_analysable":
            status = RefonteAudit.AnalysisStatus.NON_ANALYSABLE
            error = technical_report.get("reason", "")
        elif pagespeed_report["status"] != "available":
            status = RefonteAudit.AnalysisStatus.ECHEC_PARTIEL
            error = pagespeed_report.get("reason", "")
        else:
            status = RefonteAudit.AnalysisStatus.TERMINE
            error = ""

        RefonteAudit.objects.filter(pk=audit.pk).update(
            analysis_status=status,
            technical_report=technical_report,
            pagespeed_report=pagespeed_report,
            heuristic_report=heuristic_report,
            analysis_error=error,
        )
    except Exception as exc:  # noqa: BLE001 - l'analyse ne doit jamais casser le parcours.
        RefonteAudit.objects.filter(pk=audit.pk).update(
            analysis_status=RefonteAudit.AnalysisStatus.ECHEC,
            analysis_error=str(exc)[:1000],
        )
    finally:
        close_old_connections()


def analyze_site(url: str) -> dict[str, Any]:
    playwright_report = analyze_site_with_playwright(url)
    if playwright_report:
        return playwright_report

    parsed = urlparse(url)
    started = time.monotonic()

    if parsed.scheme != "https":
        https_status = "absent"
    else:
        https_status = "present"

    try:
        response = _request(url)
        status_code = response.getcode()
        html = response.read(1_500_000).decode(response.headers.get_content_charset() or "utf-8", errors="replace")
    except HTTPError as exc:
        return {
            "status": "non_analysable",
            "reason": f"HTTP {exc.code}",
            "https": https_status,
            "status_code": exc.code,
            "duration_ms": int((time.monotonic() - started) * 1000),
        }
    except (TimeoutError, URLError, ssl.SSLError, ValueError) as exc:
        return {
            "status": "non_analysable",
            "reason": str(exc)[:300],
            "https": https_status,
            "duration_ms": int((time.monotonic() - started) * 1000),
        }

    parser = MetaParser()
    parser.feed(html)
    resources = check_resources(url, parser.resources[:20])

    meta_tags = {
        "title": bool(parser.title),
        "description": bool(parser.meta.get("description")),
        "viewport": bool(parser.meta.get("viewport")),
        "og_title": bool(parser.meta.get("og:title")),
        "og_description": bool(parser.meta.get("og:description")),
        "og_image": bool(parser.meta.get("og:image")),
    }

    return {
        "status": "analysable",
        "status_code": status_code,
        "duration_ms": int((time.monotonic() - started) * 1000),
        "https": https_status,
        "meta_tags": meta_tags,
        "title": parser.title[:180],
        "failed_requests": [item for item in resources if item["status"] == "failed" or item.get("status_code", 0) >= 400],
        "slow_resources": [item for item in resources if item.get("duration_ms", 0) > SLOW_RESOURCE_SECONDS * 1000],
        "console_errors": [],
        "console_warnings": [
            "Analyse console indisponible sans moteur navigateur headless côté backend.",
        ],
    }


def analyze_site_with_playwright(url: str) -> dict[str, Any] | None:
    try:
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None

    parsed = urlparse(url)
    https_status = "present" if parsed.scheme == "https" else "absent"
    console_errors: list[str] = []
    console_warnings: list[str] = []
    failed_requests: list[dict[str, Any]] = []
    slow_resources: list[dict[str, Any]] = []
    started = time.monotonic()

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()

            page.on("console", lambda message: (
                console_errors.append(message.text[:300])
                if message.type == "error"
                else console_warnings.append(message.text[:300])
                if message.type == "warning"
                else None
            ))
            page.on("requestfailed", lambda request: failed_requests.append({
                "url": request.url,
                "status": "failed",
                "reason": request.failure or "request failed",
            }))
            page.on("response", lambda response: failed_requests.append({
                "url": response.url,
                "status": "failed",
                "status_code": response.status,
            }) if response.status >= 400 else None)

            response = page.goto(url, wait_until="networkidle", timeout=REQUEST_TIMEOUT_SECONDS * 1000)
            meta_tags = page.evaluate(
                """() => ({
                    title: Boolean(document.querySelector('title')?.textContent?.trim()),
                    description: Boolean(document.querySelector('meta[name="description"]')?.content?.trim()),
                    viewport: Boolean(document.querySelector('meta[name="viewport"]')?.content?.trim()),
                    og_title: Boolean(document.querySelector('meta[property="og:title"]')?.content?.trim()),
                    og_description: Boolean(document.querySelector('meta[property="og:description"]')?.content?.trim()),
                    og_image: Boolean(document.querySelector('meta[property="og:image"]')?.content?.trim()),
                })"""
            )
            title = page.title()[:180]
            resource_timings = page.evaluate(
                """() => performance.getEntriesByType('resource')
                    .filter((entry) => entry.duration > 2000)
                    .slice(0, 30)
                    .map((entry) => ({
                        url: entry.name,
                        status: 'slow',
                        duration_ms: Math.round(entry.duration),
                    }))"""
            )
            slow_resources.extend(resource_timings)
            browser.close()

            return {
                "status": "analysable",
                "status_code": response.status if response else None,
                "duration_ms": int((time.monotonic() - started) * 1000),
                "https": https_status,
                "meta_tags": meta_tags,
                "title": title,
                "failed_requests": failed_requests,
                "slow_resources": slow_resources,
                "console_errors": console_errors,
                "console_warnings": console_warnings,
            }
    except (PlaywrightTimeoutError, PlaywrightError) as exc:
        return {
            "status": "non_analysable",
            "reason": str(exc)[:300],
            "https": https_status,
            "duration_ms": int((time.monotonic() - started) * 1000),
            "console_errors": console_errors,
            "console_warnings": console_warnings,
            "failed_requests": failed_requests,
            "slow_resources": slow_resources,
        }


def check_resources(base_url: str, resources: list[str]) -> list[dict[str, Any]]:
    checked = []
    seen = set()

    for resource in resources:
        absolute_url = urljoin(base_url, resource)
        if absolute_url in seen:
            continue
        seen.add(absolute_url)
        started = time.monotonic()
        try:
            response = _request(absolute_url, method="HEAD", timeout=4)
            checked.append({
                "url": absolute_url,
                "status": "ok",
                "status_code": response.getcode(),
                "duration_ms": int((time.monotonic() - started) * 1000),
            })
        except HTTPError as exc:
            checked.append({
                "url": absolute_url,
                "status": "failed",
                "status_code": exc.code,
                "duration_ms": int((time.monotonic() - started) * 1000),
            })
        except Exception as exc:  # noqa: BLE001
            checked.append({
                "url": absolute_url,
                "status": "failed",
                "reason": str(exc)[:160],
                "duration_ms": int((time.monotonic() - started) * 1000),
            })

    return checked


def fetch_pagespeed(url: str) -> dict[str, Any]:
    api_key = os.environ.get("PAGESPEED_API_KEY", "").strip()

    if not api_key:
        return {"status": "unavailable", "reason": "PAGESPEED_API_KEY non configurée."}

    results = {}
    for strategy in ["mobile", "desktop"]:
        query = urlencode({"url": url, "strategy": strategy, "key": api_key})
        endpoint = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?{query}"
        try:
            response = _request(endpoint)
            payload = json.loads(response.read().decode("utf-8"))
            lighthouse = payload.get("lighthouseResult", {})
            audits = lighthouse.get("audits", {})
            results[strategy] = {
                "performance_score": _score(lighthouse.get("categories", {}).get("performance", {}).get("score")),
                "lcp": _display(audits.get("largest-contentful-paint")),
                "cls": _display(audits.get("cumulative-layout-shift")),
                "inp": _display(audits.get("interaction-to-next-paint") or audits.get("max-potential-fid")),
            }
        except Exception as exc:  # noqa: BLE001
            results[strategy] = {"status": "unavailable", "reason": str(exc)[:220]}

    if all(value.get("status") == "unavailable" for value in results.values()):
        return {"status": "unavailable", "reason": "PageSpeed indisponible.", "results": results}

    return {"status": "available", "results": results}


def build_heuristics(technical: dict[str, Any], pagespeed: dict[str, Any]) -> list[dict[str, str]]:
    meta = technical.get("meta_tags", {})
    failed_count = len(technical.get("failed_requests", []))
    slow_count = len(technical.get("slow_resources", []))
    is_https = technical.get("https") == "present"
    is_available = technical.get("status") == "analysable"
    has_pagespeed = pagespeed.get("status") == "available"

    return [
        _heuristic("Visibilité du statut système", "bon" if is_available else "non évaluable", "La page répond et expose un statut HTTP exploitable." if is_available else "Le site n'a pas pu être chargé."),
        _heuristic("Correspondance système/monde réel", "moyen" if meta.get("title") else "insuffisant", "Le titre donne un premier repère." if meta.get("title") else "Aucun titre HTML fiable n'a été détecté."),
        _heuristic("Contrôle et liberté utilisateur", "moyen", "Ce point demande une revue humaine des parcours de navigation."),
        _heuristic("Cohérence et standards", "bon" if meta.get("viewport") and is_https else "moyen", "Viewport et HTTPS détectés." if meta.get("viewport") and is_https else "Viewport ou HTTPS à vérifier."),
        _heuristic("Prévention des erreurs", "bon" if failed_count == 0 else "insuffisant", f"{failed_count} ressource(s) en erreur détectée(s)."),
        _heuristic("Reconnaissance plutôt que rappel", "bon" if meta.get("description") else "insuffisant", "Meta description présente." if meta.get("description") else "Meta description absente."),
        _heuristic("Flexibilité et efficacité d'usage", "bon" if has_pagespeed and slow_count == 0 else "moyen", "Aucune ressource lente détectée dans l'échantillon." if slow_count == 0 else f"{slow_count} ressource(s) lente(s) détectée(s)."),
        _heuristic("Design esthétique et minimaliste", "non évaluable", "Ce critère nécessite une revue visuelle humaine."),
        _heuristic("Aide au diagnostic et à la récupération d'erreurs", "moyen" if failed_count == 0 else "insuffisant", "Les erreurs techniques détectées restent limitées." if failed_count == 0 else "Des ressources échouent et peuvent produire des erreurs visibles."),
        _heuristic("Aide et documentation", "non évaluable", "La présence d'aide contextuelle doit être vérifiée manuellement."),
    ]


def _request(url: str, method: str = "GET", timeout: int = REQUEST_TIMEOUT_SECONDS):
    request = Request(url, method=method, headers={"User-Agent": "PixelProwlersAudit/1.0"})
    return urlopen(request, timeout=timeout)


def _score(value: Any) -> int | None:
    if isinstance(value, int | float):
        return round(value * 100)
    return None


def _display(audit: dict[str, Any] | None) -> str:
    if not audit:
        return "non disponible"
    return audit.get("displayValue") or str(audit.get("numericValue") or "non disponible")


def _heuristic(name: str, score: str, justification: str) -> dict[str, str]:
    return {"name": name, "score": score, "justification": justification}
