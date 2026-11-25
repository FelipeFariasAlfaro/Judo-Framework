"""
Judo JSON formatter: compact, machine/AI-friendly run results.

Usage: ``behave -f judo.behave.json_formatter:JudoJsonFormatter -o result.json``
Each failed step carries the error and the (secret-masked) last HTTP exchange.
"""
import json
from behave.formatter.base import Formatter

from ..utils.exchange import last_exchange, clear


class JudoJsonFormatter(Formatter):
    name = "judo-json"
    description = "Judo compact JSON results (AI friendly)"

    def __init__(self, stream_opener, config):
        super().__init__(stream_opener, config)
        self.stream = self.open()
        self.features = []
        self._feature = None
        self._scenario = None

    def feature(self, feature):
        self._feature = {"name": feature.name, "file": str(feature.filename), "scenarios": []}
        self.features.append(self._feature)

    def scenario(self, scenario):
        self._scenario = {"name": scenario.name, "tags": [str(t) for t in scenario.tags],
                          "status": "passed", "steps": []}
        self._feature["scenarios"].append(self._scenario)
        clear()

    def step(self, step):
        pass  # results are reported in result()

    def result(self, step):
        status = step.status.name
        entry = {"step": f"{step.keyword} {step.name}".strip(), "status": status,
                 "line": step.line, "duration": round(getattr(step, "duration", 0) or 0, 3)}
        if status in ("failed", "error"):
            entry["status"] = "failed"
            exc = step.exception
            entry["error"] = (f"{type(exc).__name__}: {exc}" if exc and not isinstance(exc, AssertionError)
                              else str(exc) if exc else (step.error_message or ""))
            entry["exchange"] = last_exchange(mask=True)
            self._scenario["status"] = "failed"
        elif status == "skipped" and self._scenario["status"] == "passed":
            self._scenario["status"] = "skipped"
        elif status == "undefined" and self._scenario["status"] != "failed":
            entry["error"] = "Undefined step"
            self._scenario["status"] = "failed"
        if self._scenario is not None:
            self._scenario["steps"].append(entry)

    def eof(self):
        pass

    def close(self):
        scenarios = [s for f in self.features for s in f["scenarios"]]
        summary = {
            "features": len(self.features),
            "scenarios": len(scenarios),
            "passed": sum(1 for s in scenarios if s["status"] == "passed"),
            "failed": sum(1 for s in scenarios if s["status"] == "failed"),
            "skipped": sum(1 for s in scenarios if s["status"] not in ("passed", "failed")),
        }
        json.dump({"summary": summary, "features": self.features}, self.stream,
                  indent=2, ensure_ascii=False, default=str)
        self.stream.write("\n")
        self.close_stream()
