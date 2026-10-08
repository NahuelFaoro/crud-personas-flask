"""Modelo de dominio para una persona."""


class Persona:
	"""Representa a una persona y mantiene sus datos individuales válidos.

	La unicidad del DNI depende de comparar varias personas, por lo que debe
	garantizarse desde el repositorio o el servicio, no desde esta instancia.
	"""

	MAX_LONGITUD_NOMBRE = 30

	def __init__(self, dni: str, nombre: str) -> None:
		self._dni = self._validar_dni(dni)
		self.nombre = nombre

	@property
	def dni(self) -> str:
		"""Devuelve el DNI, que identifica a la persona y no se modifica."""
		return self._dni

	@property
	def nombre(self) -> str:
		"""Devuelve el nombre de la persona."""
		return self._nombre

	@nombre.setter
	def nombre(self, valor: str) -> None:
		"""Actualiza el nombre si cumple las reglas de negocio."""
		if not isinstance(valor, str):
			raise TypeError("El nombre debe ser una cadena de texto.")

		nombre = valor.strip()
		if not nombre:
			raise ValueError("El nombre no puede estar vacío.")
		if len(nombre) > self.MAX_LONGITUD_NOMBRE:
			raise ValueError(
				f"El nombre no puede superar los {self.MAX_LONGITUD_NOMBRE} caracteres."
			)
		if not nombre[0].isupper():
			raise ValueError("El nombre debe comenzar con mayúscula.")
		if any(caracter.isalpha() and not caracter.islower() for caracter in nombre[1:]):
			raise ValueError("Las letras posteriores a la inicial deben ser minúsculas.")

		self._nombre = nombre
        
	@staticmethod
	def _validar_dni(valor: str) -> str:
		"""Valida y devuelve el DNI sin espacios exteriores."""
		if not isinstance(valor, str):
			raise TypeError("El DNI debe ser una cadena de texto.")

		dni = valor.strip()
		if not dni:
			raise ValueError("El DNI no puede estar vacío.")
		return dni
