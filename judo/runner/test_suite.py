"""
Test Suite - Utilidades para crear suites de tests personalizadas
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import json


class TestSuite:
    """
    Clase para definir suites de tests personalizadas
    """
    
    def __init__(self, name: str, description: str = ""):
        """
        Inicializar suite de tests
        
        Args:
            name: Nombre de la suite
            description: Descripción de la suite
        """
        self.name = name
        self.description = description
        self.features = []
        self.tags = []
        self.exclude_tags = []
        self.config = {}
        self.environments = {}
    
    def add_feature(self, feature_path: str, tags: List[str] = None):
        """
        Agregar feature a la suite
        
        Args:
            feature_path: Ruta al archivo .feature
            tags: Tags específicos para este feature
        """
        self.features.append({
            "path": feature_path,
            "tags": tags or []
        })
        return self
    
    def add_features_by_tag(self, tags: List[str]):
        """
        Agregar features por tags
        
        Args:
            tags: Tags a incluir
        """
        self.tags.extend(tags)
        return self
    
    def exclude_by_tag(self, tags: List[str]):
        """
        Excluir features por tags
        
        Args:
            tags: Tags a excluir
        """
        self.exclude_tags.extend(tags)
        return self
    
    def set_config(self, **config):
        """Configurar la suite"""
        self.config.update(config)
        return self
    
    def add_environment(self, name: str, config: Dict[str, Any]):
        """
        Agregar configuración de entorno
        
        Args:
            name: Nombre del entorno (dev, test, prod)
            config: Configuración del entorno
        """
        self.environments[name] = config
        return self
    
    def get_features_list(self) -> List[str]:
        """Obtener lista de features"""
        feature_paths = []
        
        # Features específicos
        for feature in self.features:
            feature_paths.append(feature["path"])
        
        return feature_paths
    
    def get_tags(self) -> List[str]:
        """Obtener tags de inclusión"""
        return self.tags
    
    def get_exclude_tags(self) -> List[str]:
        """Obtener tags de exclusión"""
        return self.exclude_tags
    
    def save_to_file(self, filepath: str):
        """Guardar suite a archivo JSON"""
        suite_data = {
            "name": self.name,
            "description": self.description,
            "features": self.features,
            "tags": self.tags,
            "exclude_tags": self.exclude_tags,
            "config": self.config,
            "environments": self.environments
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(suite_data, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'TestSuite':
        """Cargar suite desde archivo JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            suite_data = json.load(f)
        
        suite = cls(suite_data["name"], suite_data.get("description", ""))
        suite.features = suite_data.get("features", [])
        suite.tags = suite_data.get("tags", [])
        suite.exclude_tags = suite_data.get("exclude_tags", [])
        suite.config = suite_data.get("config", {})
        suite.environments = suite_data.get("environments", {})
        
        return suite


# Suites predefinidas comunes
class CommonSuites:
    """Suites de tests comunes predefinidas"""
    
    @staticmethod
    def smoke_tests() -> TestSuite:
        """Suite de smoke tests"""
        return TestSuite(
            name="Smoke Tests",
            description="Tests básicos de funcionalidad crítica"
        ).add_features_by_tag(["@smoke"]).set_config(
            parallel=True,
            max_workers=2,
            fail_fast=True
        )
    
    @staticmethod
    def regression_tests() -> TestSuite:
        """Suite de regression tests"""
        return TestSuite(
            name="Regression Tests", 
            description="Tests completos de regresión"
        ).add_features_by_tag(["@regression", "@api"]).exclude_by_tag(["@manual", "@slow"]).set_config(
            parallel=True,
            max_workers=4,
            timeout=600
        )
    
    @staticmethod
    def api_tests() -> TestSuite:
        """Suite de API tests"""
        return TestSuite(
            name="API Tests",
            description="Tests de APIs REST"
        ).add_features_by_tag(["@api"]).set_config(
            parallel=True,
            max_workers=6
        )
    
    @staticmethod
    def integration_tests() -> TestSuite:
        """Suite de integration tests"""
        return TestSuite(
            name="Integration Tests",
            description="Tests de integración entre servicios"
        ).add_features_by_tag(["@integration"]).exclude_by_tag(["@unit"]).set_config(
            parallel=False,  # Integración puede requerir orden
            timeout=900
        )