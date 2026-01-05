# Changelog

All notable changes to Judo Framework will be documented in this file.

## [1.5.0] - 2025-01-04

### 🚀 MAJOR RELEASE - Complete Feature Suite

**Judo Framework v1.5.0 introduces comprehensive advanced features across 3 tiers for enterprise-grade API testing.**

#### TIER 1: Robustness & Reliability ⚡

**Retry & Circuit Breaker Pattern**
- Automatic retry with configurable backoff strategies (linear, exponential, fibonacci, random)
- Circuit breaker pattern to prevent cascading failures
- Configurable failure thresholds and recovery timeouts

**Request/Response Interceptors**
- Modify requests before sending (add headers, timestamps, auth)
- Process responses before returning (logging, transformation)
- Chain multiple interceptors for complex workflows

**Rate Limiting & Throttling**
- Token bucket rate limiter for request throttling
- Fixed delay throttling between requests
- Adaptive rate limiting that respects API rate limit headers

**Advanced Assertions**
- Response time assertions (less than, between ranges)
- JSON schema validation
- Array length and content validation
- Field type and pattern matching
- Response header validation

#### TIER 2: Performance & Modern APIs 📊

**Data-Driven Testing**
- Load test data from CSV, JSON, Excel files
- Generate synthetic test data with Faker integration
- Run same test with multiple data sets
- Save results in multiple formats

**Performance Monitoring**
- Track response times (avg, median, p95, p99, min, max)
- Calculate error rates and throughput
- Performance alerts with custom callbacks
- Real-time metrics collection

**Response Caching**
- Automatic caching of GET requests
- Configurable TTL per request
- Cache statistics and management
- Reduce test execution time

**GraphQL Support**
- Native GraphQL query execution
- Mutation support
- Batch query execution
- Query and mutation builders

**WebSocket Support**
- Real-time communication testing
- Send and receive messages
- Message queuing and retrieval
- Connection management

**OAuth2 & JWT Automation**
- OAuth2 client credentials flow
- JWT token creation and verification
- Automatic token refresh
- Basic auth and API key support

#### TIER 3: Enterprise Features 🏢

**Advanced Reporting**
- Multiple report formats: HTML, JSON, JUnit XML, Allure
- Professional HTML reports with statistics
- JUnit XML for CI/CD integration
- Allure report structure generation

**API Contract Testing**
- OpenAPI/Swagger spec validation
- AsyncAPI message validation
- Endpoint discovery from specs
- Schema validation

**Chaos Engineering**
- Inject latency into requests
- Simulate error rates
- Timeout injection
- Resilience test builder

**Advanced Logging**
- Structured logging with multiple levels
- Request/response logging to files
- Performance metric logging
- Detailed error tracking

#### New Installation Options

```bash
# Excel support
pip install judo-framework[excel]

# WebSocket support
pip install judo-framework[websocket]

# GraphQL support
pip install judo-framework[graphql]

# All features
pip install judo-framework[full]
```

#### Usage Examples

**Retry with Circuit Breaker:**
```python
from judo.core.judo_extended import JudoExtended

judo = JudoExtended()
judo.set_retry_policy(max_retries=3, backoff_strategy="exponential")
cb = judo.create_circuit_breaker("api", failure_threshold=5)
```

**Rate Limiting:**
```python
judo.set_rate_limit(requests_per_second=10)
judo.set_throttle(delay_ms=100)
```

**Data-Driven Testing:**
```python
results = judo.run_data_driven_test("test_data.csv", test_function)
```

**Performance Monitoring:**
```python
judo.set_performance_alert("response_time", threshold=500)
metrics = judo.get_performance_metrics()
```

**GraphQL:**
```python
response = judo.graphql_query(query, variables={"id": "123"})
```

**OAuth2:**
```python
judo.setup_oauth2(client_id="...", client_secret="...", token_url="...")
```

**Chaos Engineering:**
```python
judo.enable_chaos()
judo.inject_latency(min_ms=100, max_ms=500)
judo.inject_error_rate(percentage=10)
```

#### Breaking Changes
- None - fully backward compatible with v1.4.0

#### Migration Guide
All new features are opt-in. Existing code continues to work without changes.

---

## [1.4.0] - 2025-01-04

### 🔄 BREAKING CHANGE - Playwright Removed as Mandatory Dependency

**Playwright is no longer installed by default. Judo Framework is now a pure API Testing Framework.**

#### Rationale
- Judo Framework's primary focus is **API Testing**, not UI Testing
- Playwright was installed by default but only used by ~20% of users
- Removing it reduces installation size by 90% (150MB → 10MB)
- Reduces installation time by 95% (2-3 minutes → 10-20 seconds)
- Eliminates conflicts with users who prefer Selenium, Cypress, or other tools

#### What Changed
- ❌ Removed `playwright>=1.32.0` from `install_requires` in setup.py
- ❌ Removed `judo/playwright/` module completely
- ❌ Removed Playwright examples and documentation
- ✅ Framework now focuses exclusively on API Testing

#### Impact
- ✅ **Faster Installation**: 10-20 seconds instead of 2-3 minutes
- ✅ **Smaller Size**: 10MB instead of 150MB
- ✅ **No Conflicts**: Works with Selenium, Cypress, Puppeteer, or any UI testing tool
- ✅ **Clearer Focus**: Judo = API Testing Framework

---

## [1.3.42] - 2024-12-20

### ✨ Features
- Smart .env file loading from project root
- Improved environment variable support
- Enhanced HTML reports with professional branding

---

## [1.3.0] - 2024-11-01

### ✨ Initial Release
- Complete API testing framework
- BDD/Gherkin support with Behave
- 100+ predefined steps in English and Spanish
- Professional HTML reports
- Mock server integration
- Request/Response logging
