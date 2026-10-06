"""Repositorio en memoria para personas."""

from model.persona import Persona


class DniDuplicadoError(ValueError):
	"""Se lanza cuando se intenta guardar un DNI que ya está registrado."""


class RepositorioPersonas:
	"""Mantiene personas en una lista durante la ejecución de la aplicación."""

	def __init__(self) -> None:
		self.__personas: list[Persona] = []
		self.__cargar_datos_prueba()

	def __cargar_datos_prueba(self) -> None:
		"""Agrega cinco personas iniciales para probar la API."""
		self.__personas.extend(
			[
				Persona("10000001", "Ana"),
				Persona("10000002", "Luis"),
				Persona("10000003", "María"),
				Persona("10000004", "Pedro"),
				Persona("10000005", "Sofía"),
			]
		)

	def guardar(self, persona: Persona) -> None:
		"""Agrega una persona, siempre que su DNI no esté registrado."""
		if self.obtener_por_dni(persona.dni) is not None:
			raise DniDuplicadoError(
				f"Ya existe una persona con DNI {persona.dni}."
			)

		self.__personas.append(persona)

	def obtener_por_dni(self, dni: str) -> Persona | None:
		"""Busca una persona por DNI y devuelve None si no existe."""
		dni = self._validar_dni(dni)
		for persona in self.__personas:
			if persona.dni == dni:
				return persona
		return None

	def obtener_todos(self) -> list[Persona]:
		"""Devuelve una copia de la lista para proteger el estado interno."""
		return self.__personas.copy()

	def eliminar(self, dni: str) -> bool:
		"""Elimina por DNI e indica si se encontró la persona."""
		persona = self.obtener_por_dni(dni)
		if persona is None:
			return False

		self.__personas.remove(persona)
		return True

	@staticmethod
	def _validar_dni(dni: str) -> str:
		if not isinstance(dni, str):
			raise TypeError("El DNI debe ser una cadena de texto.")
		dni = dni.strip()
		if not dni:
			raise ValueError("El DNI no puede estar vacío.")
		return dni