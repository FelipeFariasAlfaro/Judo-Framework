"""
GraphQL Support
Native GraphQL query support
"""

import json
from typing import Dict, Any, Optional, List


class GraphQLClient:
    """GraphQL client for API testing"""
    
    def __init__(self, http_client):
        """
        Initialize GraphQL client
        
        Args:
            http_client: Judo HTTP client instance
        """
        self.http_client = http_client
    
    def query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute GraphQL query
        
        Args:
            query: GraphQL query string
            variables: Query variables
            operation_name: Operation name
            **kwargs: Additional request parameters
        
        Returns:
            GraphQL response
        """
        payload = {
            "query": query
        }
        
        if variables:
            payload["variables"] = variables
        
        if operation_name:
            payload["operationName"] = operation_name
        
        # Set content type
        headers = kwargs.get("headers", {})
        headers["Content-Type"] = "application/json"
        kwargs["headers"] = headers
        
        # Make request
        response = self.http_client.post(
            self.http_client.judo.base_url,
            json=payload,
            **kwargs
        )
        
        return response.json if hasattr(response, 'json') else response
    
    def mutation(
        self,
        mutation: str,
        variables: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute GraphQL mutation
        
        Args:
            mutation: GraphQL mutation string
            variables: Mutation variables
            operation_name: Operation name
            **kwargs: Additional request parameters
        
        Returns:
            GraphQL response
        """
        return self.query(mutation, variables, operation_name, **kwargs)
    
    def batch_query(
        self,
        queries: List[Dict[str, Any]],
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Execute multiple GraphQL queries in batch
        
        Args:
            queries: List of query dicts with 'query', 'variables', 'operationName'
            **kwargs: Additional request parameters
        
        Returns:
            List of responses
        """
        payload = [
            {
                "query": q.get("query"),
                "variables": q.get("variables"),
                "operationName": q.get("operationName")
            }
            for q in queries
        ]
        
        # Set content type
        headers = kwargs.get("headers", {})
        headers["Content-Type"] = "application/json"
        kwargs["headers"] = headers
        
        # Make request
        response = self.http_client.post(
            self.http_client.judo.base_url,
            json=payload,
            **kwargs
        )
        
        return response.json if hasattr(response, 'json') else response
    
    @staticmethod
    def build_query(
        operation_name: str,
        fields: List[str],
        variables: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Build GraphQL query string
        
        Args:
            operation_name: Query operation name
            fields: List of fields to query
            variables: Query variables with types
        
        Returns:
            GraphQL query string
        """
        query_parts = [f"query {operation_name}"]
        
        if variables:
            var_defs = ", ".join(
                f"${name}: {var_type}"
                for name, var_type in variables.items()
            )
            query_parts.append(f"({var_defs})")
        
        query_parts.append("{")
        query_parts.extend(fields)
        query_parts.append("}")
        
        return " ".join(query_parts)
    
    @staticmethod
    def build_mutation(
        operation_name: str,
        mutation_name: str,
        input_fields: Dict[str, str],
        return_fields: List[str],
        variables: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Build GraphQL mutation string
        
        Args:
            operation_name: Mutation operation name
            mutation_name: Mutation name
            input_fields: Input fields with types
            return_fields: Fields to return
            variables: Mutation variables with types
        
        Returns:
            GraphQL mutation string
        """
        mutation_parts = [f"mutation {operation_name}"]
        
        all_vars = variables or {}
        all_vars.update(input_fields)
        
        if all_vars:
            var_defs = ", ".join(
                f"${name}: {var_type}"
                for name, var_type in all_vars.items()
            )
            mutation_parts.append(f"({var_defs})")
        
        mutation_parts.append("{")
        
        # Build mutation call
        input_vars = ", ".join(
            f"{name}: ${name}"
            for name in input_fields.keys()
        )
        mutation_parts.append(f"{mutation_name}({input_vars}) {{")
        mutation_parts.extend(return_fields)
        mutation_parts.append("}")
        
        mutation_parts.append("}")
        
        return " ".join(mutation_parts)
