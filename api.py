"""API REST de personas implementada con Flask."""

from flask import Flask, jsonify, request, url_for

from model.persona import Persona
from repository.personas_repository import DniDuplicadoError
from service.personas_service import PersonasService


def crear_app(servicio: PersonasService | None = None) -> Flask:
	"""Crea la aplicación Flask; acepta un servicio alternativo para pruebas."""
	app = Flask(__name__)
	personas_service = servicio or PersonasService()

	def serializar(persona: Persona) -> dict[str, str]:
		return {"dni": persona.dni, "nombre": persona.nombre}

	@app.get("/personas")
	def obtener_personas():
		personas = personas_service.obtener_todos()
		return jsonify([serializar(persona) for persona in personas]), 200

	@app.get("/personas/<string:dni>")
	def obtener_persona(dni: str):
		try:
			persona = personas_service.obtener_por_dni(dni)
		except (TypeError, ValueError) as error:
			return jsonify(error=str(error)), 400

		if persona is None:
			return jsonify(error="No se encontró una persona con ese DNI."), 404
		return jsonify(serializar(persona)), 200

	@app.post("/personas")
	def agregar_persona():
		datos = request.get_json(silent=True)
		if not isinstance(datos, dict):
			return jsonify(error="El cuerpo debe ser un objeto JSON."), 400

		if "dni" not in datos or "nombre" not in datos:
			return jsonify(error="Se requieren los campos 'dni' y 'nombre'."), 400

		try:
			persona = personas_service.crear_persona(
				dni=datos["dni"], nombre=datos["nombre"]
			)
		except DniDuplicadoError as error:
			return jsonify(error=str(error)), 409
		except (TypeError, ValueError) as error:
			return jsonify(error=str(error)), 400

		respuesta = jsonify(serializar(persona))
		respuesta.status_code = 201
		respuesta.headers["Location"] = url_for(
			"obtener_persona", dni=persona.dni
		)
		return respuesta

	return app


app = crear_app()


if __name__ == "__main__":
	app.run(debug=True)
