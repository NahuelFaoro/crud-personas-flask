"""Servicios de aplicación para las operaciones de personas."""

from model.persona import Persona
from repository.personas_repository import RepositorioPersonas


class PersonasService:
    """Coordina las reglas del modelo con el repositorio."""

    def __init__(self, repositorio: RepositorioPersonas | None = None) -> None:
        self._repositorio = repositorio or RepositorioPersonas()

    def obtener_todos(self) -> list[Persona]:
        return self._repositorio.obtener_todos()

    def obtener_por_dni(self, dni: str) -> Persona | None:
        return self._repositorio.obtener_por_dni(dni)

    def crear_persona(self, dni: str, nombre: str) -> Persona:
        persona = Persona(dni=dni, nombre=nombre)
        self._repositorio.guardar(persona)
        return persona

    def actualizar_nombre(self, dni: str, nombre: str) -> Persona | None:
        persona = self._repositorio.obtener_por_dni(dni)
        if persona is None:
            return None

        persona.nombre = nombre
        return persona

    def eliminar_persona(self, dni: str) -> bool:
        return self._repositorio.eliminar(dni)