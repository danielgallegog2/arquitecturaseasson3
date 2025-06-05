from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

# Enumeraciones para el sistema
class TipoIncidencia(Enum):
    HARDWARE = "hardware"
    SOFTWARE = "software"
    RED = "red"
    SEGURIDAD = "seguridad"

class Prioridad(Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"

class Estado(Enum):
    ABIERTA = "abierta"
    EN_PROGRESO = "en_progreso"
    CERRADA = "cerrada"

# Clase base abstracta para las incidencias
class Incidencia(ABC):
    """Clase abstracta que define la interfaz común para todas las incidencias"""
    
    def __init__(self, titulo: str, descripcion: str, usuario_id: int):
        self.titulo = titulo
        self.descripcion = descripcion
        self.usuario_id = usuario_id
        self.estado = Estado.ABIERTA
        self.creado_en = datetime.now()
        self.prioridad = Prioridad.MEDIA
    
    @abstractmethod
    def calcular_tiempo_estimado(self) -> int:
        """Calcula el tiempo estimado de resolución en horas"""
        pass
    
    @abstractmethod
    def obtener_tecnico_especializado(self) -> str:
        """Retorna el tipo de técnico especializado para esta incidencia"""
        pass
    
    def obtener_informacion(self) -> dict:
        """Retorna información básica de la incidencia"""
        return {
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'estado': self.estado.value,
            'prioridad': self.prioridad.value,
            'creado_en': self.creado_en.strftime('%Y-%m-%d %H:%M:%S'),
            'tiempo_estimado': self.calcular_tiempo_estimado(),
            'tecnico_especializado': self.obtener_tecnico_especializado()
        }

# Clases concretas de incidencias
class IncidenciaHardware(Incidencia):
    """Incidencia relacionada con problemas de hardware"""
    
    def __init__(self, titulo: str, descripcion: str, usuario_id: int):
        super().__init__(titulo, descripcion, usuario_id)
        self.tipo = TipoIncidencia.HARDWARE
        self.prioridad = Prioridad.ALTA  # Hardware suele ser prioritario
    
    def calcular_tiempo_estimado(self) -> int:
        """Hardware requiere más tiempo por diagnóstico físico"""
        return 4  # 4 horas promedio
    
    def obtener_tecnico_especializado(self) -> str:
        return "Técnico de Hardware"

class IncidenciaSoftware(Incidencia):
    """Incidencia relacionada con problemas de software"""
    
    def __init__(self, titulo: str, descripcion: str, usuario_id: int):
        super().__init__(titulo, descripcion, usuario_id)
        self.tipo = TipoIncidencia.SOFTWARE
        self.prioridad = Prioridad.MEDIA
    
    def calcular_tiempo_estimado(self) -> int:
        """Software puede resolverse más rápido"""
        return 2  # 2 horas promedio
    
    def obtener_tecnico_especializado(self) -> str:
        return "Desarrollador/Técnico de Software"

class IncidenciaRed(Incidencia):
    """Incidencia relacionada con problemas de red"""
    
    def __init__(self, titulo: str, descripcion: str, usuario_id: int):
        super().__init__(titulo, descripcion, usuario_id)
        self.tipo = TipoIncidencia.RED
        self.prioridad = Prioridad.CRITICA  # Red afecta a muchos usuarios
    
    def calcular_tiempo_estimado(self) -> int:
        """Red requiere diagnóstico de infraestructura"""
        return 3  # 3 horas promedio
    
    def obtener_tecnico_especializado(self) -> str:
        return "Administrador de Redes"

class IncidenciaSeguridad(Incidencia):
    """Incidencia relacionada con problemas de seguridad"""
    
    def __init__(self, titulo: str, descripcion: str, usuario_id: int):
        super().__init__(titulo, descripcion, usuario_id)
        self.tipo = TipoIncidencia.SEGURIDAD
        self.prioridad = Prioridad.CRITICA  # Seguridad es crítica
    
    def calcular_tiempo_estimado(self) -> int:
        """Seguridad requiere análisis detallado"""
        return 6  # 6 horas promedio
    
    def obtener_tecnico_especializado(self) -> str:
        return "Especialista en Seguridad"

# Factory Method - Clase abstracta creadora
class CreadorIncidencias(ABC):
    """Clase abstracta que define el método factory para crear incidencias"""
    
    @abstractmethod
    def crear_incidencia(self, titulo: str, descripcion: str, usuario_id: int) -> Incidencia:
        """Método factory abstracto para crear incidencias"""
        pass
    
    def procesar_incidencia(self, titulo: str, descripcion: str, usuario_id: int) -> dict:
        """Método que utiliza el factory method para procesar una incidencia"""
        incidencia = self.crear_incidencia(titulo, descripcion, usuario_id)
        
        # Lógica adicional de procesamiento
        print(f"Procesando incidencia: {incidencia.titulo}")
        print(f"Asignando a: {incidencia.obtener_tecnico_especializado()}")
        print(f"Tiempo estimado: {incidencia.calcular_tiempo_estimado()} horas")
        
        return incidencia.obtener_informacion()

# Clases creadoras concretas
class CreadorIncidenciaHardware(CreadorIncidencias):
    """Factory concreto para crear incidencias de hardware"""
    
    def crear_incidencia(self, titulo: str, descripcion: str, usuario_id: int) -> IncidenciaHardware:
        return IncidenciaHardware(titulo, descripcion, usuario_id)

class CreadorIncidenciaSoftware(CreadorIncidencias):
    """Factory concreto para crear incidencias de software"""
    
    def crear_incidencia(self, titulo: str, descripcion: str, usuario_id: int) -> IncidenciaSoftware:
        return IncidenciaSoftware(titulo, descripcion, usuario_id)

class CreadorIncidenciaRed(CreadorIncidencias):
    """Factory concreto para crear incidencias de red"""
    
    def crear_incidencia(self, titulo: str, descripcion: str, usuario_id: int) -> IncidenciaRed:
        return IncidenciaRed(titulo, descripcion, usuario_id)

class CreadorIncidenciaSeguridad(CreadorIncidencias):
    """Factory concreto para crear incidencias de seguridad"""
    
    def crear_incidencia(self, titulo: str, descripcion: str, usuario_id: int) -> IncidenciaSeguridad:
        return IncidenciaSeguridad(titulo, descripcion, usuario_id)

# Clase gestora que utiliza el patrón Factory Method
class GestorIncidencias:
    """Clase que gestiona la creación de incidencias usando Factory Method"""
    
    def __init__(self):
        # Mapeo de tipos a sus respectivos factories
        self._factories = {
            TipoIncidencia.HARDWARE: CreadorIncidenciaHardware(),
            TipoIncidencia.SOFTWARE: CreadorIncidenciaSoftware(),
            TipoIncidencia.RED: CreadorIncidenciaRed(),
            TipoIncidencia.SEGURIDAD: CreadorIncidenciaSeguridad()
        }
    
    def crear_incidencia(self, tipo: TipoIncidencia, titulo: str, descripcion: str, usuario_id: int) -> dict:
        """Crea una incidencia del tipo especificado"""
        if tipo not in self._factories:
            raise ValueError(f"Tipo de incidencia no soportado: {tipo}")
        
        factory = self._factories[tipo]
        return factory.procesar_incidencia(titulo, descripcion, usuario_id)
    
    def obtener_tipos_disponibles(self) -> list:
        """Retorna los tipos de incidencias disponibles"""
        return [tipo.value for tipo in self._factories.keys()]

# Ejemplo de uso del patrón
def main():
    """Función principal que demuestra el uso del patrón Factory Method"""
    print("=== Sistema de Gestión de Incidencias - Patrón Factory Method ===\n")
    
    # Crear el gestor de incidencias
    gestor = GestorIncidencias()
    
    # Ejemplos de creación de diferentes tipos de incidencias
    incidencias_ejemplo = [
        {
            'tipo': TipoIncidencia.HARDWARE,
            'titulo': 'Falla en impresora HP LaserJet',
            'descripcion': 'La impresora no responde y muestra error de papel atascado',
            'usuario_id': 1
        },
        {
            'tipo': TipoIncidencia.SOFTWARE,
            'titulo': 'Error en Microsoft Excel',
            'descripcion': 'Excel se cierra inesperadamente al abrir archivos grandes',
            'usuario_id': 2
        },
        {
            'tipo': TipoIncidencia.RED,
            'titulo': 'Conexión lenta a internet',
            'descripcion': 'Velocidad de conexión muy baja en toda la oficina',
            'usuario_id': 3
        },
        {
            'tipo': TipoIncidencia.SEGURIDAD,
            'titulo': 'Posible intento de phishing',
            'descripcion': 'Empleado recibió email sospechoso solicitando credenciales',
            'usuario_id': 4
        }
    ]
    
    # Procesar cada incidencia
    for i, datos in enumerate(incidencias_ejemplo, 1):
        print(f"--- Incidencia {i} ---")
        info_incidencia = gestor.crear_incidencia(
            datos['tipo'],
            datos['titulo'],
            datos['descripcion'],
            datos['usuario_id']
        )
        
        print(f"Información de la incidencia:")
        for clave, valor in info_incidencia.items():
            print(f"  {clave}: {valor}")
        print()
    
    print("Tipos de incidencias disponibles:", gestor.obtener_tipos_disponibles())

if __name__ == "__main__":
    main()