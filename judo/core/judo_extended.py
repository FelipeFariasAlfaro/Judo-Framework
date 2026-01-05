"""
Extended Judo Framework with all advanced features
Integrates Tier 1, 2, and 3 features
"""

from typing import Any, Dict, List, Optional, Callable
from .judo import Judo
from ..features.retry import RetryPolicy, CircuitBreaker, BackoffStrategy
from ..features.interceptors import InterceptorChain, RequestInterceptor, ResponseInterceptor
from ..features.rate_limiter import RateLimiter, Throttle, AdaptiveRateLimiter
from ..features.assertions import AdvancedAssertions
from ..features.data_driven import DataDrivenTesting
from ..features.performance import PerformanceMonitor, PerformanceAlert
from ..features.caching import ResponseCache
from ..features.graphql import GraphQLClient
from ..features.websocket import WebSocketClient
from ..features.auth import OAuth2Handler, JWTHandler, BasicAuthHandler, APIKeyHandler
from ..features.reporting import ReportGenerator
from ..features.contract import ContractValidator
from ..features.chaos import ChaosInjector, ResilienceTestBuilder
from ..features.logging import AdvancedLogger, RequestLogger


class JudoExtended(Judo):
    """
    Extended Judo Framework with all advanced features
    Includes Tier 1, 2, and 3 functionality
    """
    
    def __init__(self, base_url: str = None, config: Dict = None, enable_reporting: bool = True):
        """Initialize extended Judo instance"""
        super().__init__(base_url, config, enable_reporting)
        
        # Tier 1: Retry & Circuit Breaker
        self.retry_policy = None
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        
        # Tier 1: Interceptors
        self.interceptor_chain = InterceptorChain()
        
        # Tier 1: Rate Limiting
        self.rate_limiter = None
        self.throttle = None
        self.adaptive_rate_limiter = None
        
        # Tier 1: Advanced Assertions
        self.assertions = AdvancedAssertions()
        
        # Tier 2: Data-Driven Testing
        self.data_driven = DataDrivenTesting()
        
        # Tier 2: Performance Monitoring
        self.performance_monitor = PerformanceMonitor()
        
        # Tier 2: Response Caching
        self.cache = ResponseCache()
        
        # Tier 2: GraphQL
        self.graphql = GraphQLClient(self.http_client)
        
        # Tier 2: WebSocket
        self.websocket = None
        
        # Tier 2: Authentication
        self.oauth2_handler = None
        self.jwt_handler = None
        self.basic_auth_handler = None
        self.api_key_handler = None
        
        # Tier 3: Reporting
        self.report_generator = None
        
        # Tier 3: Contract Testing
        self.contract_validator = None
        
        # Tier 3: Chaos Engineering
        self.chaos_injector = ChaosInjector()
        
        # Tier 3: Advanced Logging
        self.logger = AdvancedLogger("judo")
        self.request_logger = None
    
    # ==================== TIER 1: Retry & Circuit Breaker ====================
    
    def set_retry_policy(
        self,
        max_retries: int = 3,
        backoff_strategy: str = "exponential",
        initial_delay: float = 1.0,
        max_delay: float = 60.0
    ) -> "JudoExtended":
        """Set retry policy"""
        self.retry_policy = RetryPolicy(
            max_retries=max_retries,
            backoff_strategy=BackoffStrategy[backoff_strategy.upper()],
            initial_delay=initial_delay,
            max_delay=max_delay
        )
        return self
    
    def create_circuit_breaker(
        self,
        name: str,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout: int = 60
    ) -> CircuitBreaker:
        """Create circuit breaker"""
        cb = CircuitBreaker(
            failure_threshold=failure_threshold,
            success_threshold=success_threshold,
            timeout=timeout,
            name=name
        )
        self.circuit_breakers[name] = cb
        return cb
    
    def get_circuit_breaker(self, name: str) -> Optional[CircuitBreaker]:
        """Get circuit breaker by name"""
        return self.circuit_breakers.get(name)
    
    # ==================== TIER 1: Interceptors ====================
    
    def add_request_interceptor(self, interceptor: RequestInterceptor) -> "JudoExtended":
        """Add request interceptor"""
        self.interceptor_chain.add_request_interceptor(interceptor)
        return self
    
    def add_response_interceptor(self, interceptor: ResponseInterceptor) -> "JudoExtended":
        """Add response interceptor"""
        self.interceptor_chain.add_response_interceptor(interceptor)
        return self
    
    # ==================== TIER 1: Rate Limiting ====================
    
    def set_rate_limit(self, requests_per_second: float = 10.0) -> "JudoExtended":
        """Set rate limit"""
        self.rate_limiter = RateLimiter(requests_per_second)
        return self
    
    def set_throttle(self, delay_ms: float = 100) -> "JudoExtended":
        """Set throttle"""
        self.throttle = Throttle(delay_ms)
        return self
    
    def set_adaptive_rate_limit(self, initial_rps: float = 10.0) -> "JudoExtended":
        """Set adaptive rate limit"""
        self.adaptive_rate_limiter = AdaptiveRateLimiter(initial_rps)
        return self
    
    # ==================== TIER 1: Advanced Assertions ====================
    
    def assert_response_time_less_than(self, max_ms: float, response: Any = None):
        """Assert response time"""
        self.assertions.assert_response_time_less_than(max_ms, response)
        return self
    
    def assert_json_schema_valid(self, schema: Dict, response: Any = None):
        """Assert JSON schema"""
        self.assertions.assert_json_schema_valid(schema, response)
        return self
    
    # ==================== TIER 2: Data-Driven Testing ====================
    
    def run_data_driven_test(
        self,
        data_source: str,
        test_func: Callable,
        source_type: Optional[str] = None
    ) -> List[Dict]:
        """Run data-driven test"""
        return self.data_driven.run_with_data_source(data_source, test_func, source_type)
    
    def generate_test_data(self, count: int, template: Dict) -> List[Dict]:
        """Generate test data"""
        return self.data_driven.generate_test_data(count, template)
    
    # ==================== TIER 2: Performance Monitoring ====================
    
    def get_performance_metrics(self) -> Dict:
        """Get performance metrics"""
        return self.performance_monitor.get_metrics()
    
    def set_performance_alert(self, metric: str, threshold: float, callback: Optional[Callable] = None):
        """Set performance alert"""
        alert = PerformanceAlert(metric, threshold, callback)
        self.performance_monitor.add_alert(alert)
        return self
    
    # ==================== TIER 2: Response Caching ====================
    
    def enable_cache(self, ttl: Optional[int] = 300) -> "JudoExtended":
        """Enable response caching"""
        self.cache.enabled = True
        self.cache.default_ttl = ttl
        return self
    
    def disable_cache(self) -> "JudoExtended":
        """Disable response caching"""
        self.cache.disable()
        return self
    
    # ==================== TIER 2: GraphQL ====================
    
    def graphql_query(self, query: str, variables: Optional[Dict] = None, **kwargs) -> Dict:
        """Execute GraphQL query"""
        return self.graphql.query(query, variables, **kwargs)
    
    def graphql_mutation(self, mutation: str, variables: Optional[Dict] = None, **kwargs) -> Dict:
        """Execute GraphQL mutation"""
        return self.graphql.mutation(mutation, variables, **kwargs)
    
    # ==================== TIER 2: WebSocket ====================
    
    def connect_websocket(self, url: str, timeout: float = 5.0) -> Optional[WebSocketClient]:
        """Connect to WebSocket"""
        self.websocket = WebSocketClient(url)
        if self.websocket.connect(timeout):
            return self.websocket
        return None
    
    # ==================== TIER 2: Authentication ====================
    
    def setup_oauth2(
        self,
        client_id: str,
        client_secret: str,
        token_url: str,
        scope: str = ""
    ) -> "JudoExtended":
        """Setup OAuth2"""
        self.oauth2_handler = OAuth2Handler(client_id, client_secret, token_url, scope)
        return self
    
    def setup_jwt(
        self,
        secret: str,
        algorithm: str = "HS256",
        auto_refresh: bool = True
    ) -> "JudoExtended":
        """Setup JWT"""
        self.jwt_handler = JWTHandler(secret, algorithm, auto_refresh)
        return self
    
    def setup_basic_auth(self, username: str, password: str) -> "JudoExtended":
        """Setup basic authentication"""
        self.basic_auth_handler = BasicAuthHandler(username, password)
        return self
    
    def setup_api_key(self, key: str, header_name: str = "X-API-Key") -> "JudoExtended":
        """Setup API key authentication"""
        self.api_key_handler = APIKeyHandler(key, header_name)
        return self
    
    # ==================== TIER 3: Reporting ====================
    
    def generate_reports(self, results: List[Dict], output_dir: str):
        """Generate all report formats"""
        self.report_generator = ReportGenerator(results)
        self.report_generator.generate_all(output_dir)
    
    # ==================== TIER 3: Contract Testing ====================
    
    def validate_against_openapi(self, spec_file: str) -> "JudoExtended":
        """Setup OpenAPI contract validation"""
        self.contract_validator = ContractValidator(spec_file)
        return self
    
    # ==================== TIER 3: Chaos Engineering ====================
    
    def enable_chaos(self) -> "JudoExtended":
        """Enable chaos injection"""
        self.chaos_injector.enable()
        return self
    
    def disable_chaos(self) -> "JudoExtended":
        """Disable chaos injection"""
        self.chaos_injector.disable()
        return self
    
    def inject_latency(self, min_ms: float = 0, max_ms: float = 100) -> "JudoExtended":
        """Inject latency"""
        self.chaos_injector.inject_latency(min_ms, max_ms)
        return self
    
    def inject_error_rate(self, percentage: float = 10.0) -> "JudoExtended":
        """Inject error rate"""
        self.chaos_injector.inject_error_rate(percentage)
        return self
    
    def inject_timeout(self, probability: float = 0.05) -> "JudoExtended":
        """Inject timeout"""
        self.chaos_injector.inject_timeout(probability)
        return self
    
    # ==================== TIER 3: Advanced Logging ====================
    
    def set_log_level(self, level: str) -> "JudoExtended":
        """Set logging level"""
        self.logger.set_level(level)
        return self
    
    def enable_request_logging(self, log_dir: str = "request_logs") -> "JudoExtended":
        """Enable request logging"""
        self.request_logger = RequestLogger(log_dir)
        return self
