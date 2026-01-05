# Judo Framework v1.5.1 - Bug Fix Summary

## 🐛 Issue Fixed

**AmbiguousStep Error**: Duplicate step definitions prevented test execution

### Error Message
```
behave.step_registry.AmbiguousStep: @step('circuit breaker "{name}" should be in state {state}') 
has already been defined in existing step @step('circuit breaker "{name}" should be in state {state}') 
at ../../../../AppData/Roaming/Python/Python313/site-packages/judo/behave/steps.py:716
```

---

## ✅ Changes Made

### 1. Removed Duplicate Circuit Breaker Step
- **Location**: `judo/behave/steps.py` lines 1268-1281
- **Removed**: `step_validate_circuit_breaker_state_fixed()` function
- **Reason**: Duplicate of `step_validate_circuit_breaker_state()` at line 716
- **Impact**: Circuit breaker validation now uses single, unified step definition

### 2. Removed Duplicate Performance Metrics Step
- **Location**: `judo/behave/steps.py` lines 1419-1427
- **Removed**: `step_validate_performance_metrics_alt()` function
- **Reason**: Duplicate of `step_validate_performance_metrics()` at line 878
- **Impact**: Performance metrics validation now uses single, unified step definition

### 3. Updated Version Numbers
- **setup.py**: `1.5.0` → `1.5.1`
- **pyproject.toml**: `1.5.0` → `1.5.1`
- **CHANGELOG.md**: Added v1.5.1 entry

---

## 📊 Verification

### Before Fix
```
❌ AmbiguousStep error on step registration
❌ Tests cannot execute
❌ Behave fails during hook loading
```

### After Fix
```
✅ All step definitions are unique
✅ No conflicts in step registry
✅ Tests execute successfully
✅ 100+ step definitions properly registered
```

---

## 🧪 Testing

The fix has been verified to:
- ✅ Remove all duplicate step definitions
- ✅ Maintain all functionality (no features removed)
- ✅ Allow test execution without errors
- ✅ Support all 3 showcase files (English, Spanish, Mixed)

---

## 📦 Release Information

- **Version**: 1.5.1
- **Release Date**: January 4, 2026
- **Type**: Bug Fix (Patch Release)
- **Breaking Changes**: None
- **Backward Compatible**: Yes

---

## 🚀 Installation

```bash
pip install judo-framework==1.5.1
```

---

## 📝 Notes

- This is a critical bug fix for v1.5.0
- All users of v1.5.0 should upgrade to v1.5.1
- No changes to functionality or API
- All existing tests will work without modification
