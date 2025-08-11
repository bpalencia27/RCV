from __future__ import annotations
from .models import AsistenteResultado, Paciente, ResumenRiesgo
from .labs import agenda_labs
from .scoring import calcula_puntaje
from .risk import clasificar_riesgo_cv_4_pasos, ascvd_ajustado
from .tfg import crcl_cockcroft_gault


def _programa_prioritario(p: Paciente) -> str:
	# Heurística mínima: si creatinina presente => ERC, else HTA si PAS, else GENERAL
	if any(l.nombre == "CREATININA EN SUERO U OTROS" for l in p.labs):
		return "ERC"
	if any(l.nombre == "PRESION ARTERIAL SISTOLICA" for l in p.labs):
		return "HTA"
	return "GENERAL"


def analizar_paciente(paciente: Paciente) -> AsistenteResultado:
	"""Analiza paciente y retorna estructura unificada AsistenteResultado."""
	agenda = agenda_labs(paciente)
	puntaje = calcula_puntaje(paciente)
	riesgo_cat = clasificar_riesgo_cv_4_pasos(paciente)
	programa = _programa_prioritario(paciente)
	crcl = crcl_cockcroft_gault(paciente)
	resumen_riesgo = ResumenRiesgo(
		riesgo_categoria=riesgo_cat,
		puntaje=puntaje,
		ascvd=ascvd_ajustado(paciente),
		aclaramiento_creatinina=crcl,
		agenda=agenda,
	)

	# Construir razones principales para justificar categoría de riesgo
	_reasons = []
	if any(l.nombre == "COLESTEROL LDL" and l.valor >= 130 for l in paciente.labs):
		_reasons.append("LDL elevado")
	if paciente.has_dm:
		_reasons.append("Diabetes mellitus")
	if any(l.nombre == "HEMOGLOBINA GLICOSILADA (HBA1C)" and l.valor >= 7 for l in paciente.labs):
		_reasons.append("HbA1c elevada")
	if any(l.nombre == "PRESION ARTERIAL SISTOLICA" and l.valor >= 140 for l in paciente.labs):
		_reasons.append("Hipertensión sistólica")
	if any(l.nombre == "CREATININA EN SUERO U OTROS" and l.valor >= 1.3 for l in paciente.labs):
		_reasons.append("Función renal reducida")
	if paciente.estadio_erc:
		_reasons.append(f"ERC estadio {paciente.estadio_erc}")
	if crcl is not None and crcl < 60:
		_reasons.append(f"Aclaramiento <60 ({crcl} ml/min)")

	# Cálculo de estadio ERC derivado si no provisto explícitamente
	if not paciente.estadio_erc and crcl is not None:
		if crcl >= 90:
			estadio_calc = 1
		elif crcl >= 60:
			estadio_calc = 2
		elif crcl >= 45:
			estadio_calc = "3a"
		elif crcl >= 30:
			estadio_calc = "3b"
		elif crcl >= 15:
			estadio_calc = 4
		else:
			estadio_calc = 5
		_reasons.append(f"ERC estadio {estadio_calc} (calculado)")
	justificacion_riesgo = (
		f"Riesgo {riesgo_cat} por: " + ", ".join(_reasons)
		if _reasons
		else f"Riesgo {riesgo_cat}"
	)
	return AsistenteResultado(
		version="v2.0",
		resumen="Análisis inicial",
		programa=programa,
		riesgo=resumen_riesgo,
		puntaje_total=puntaje,
		agenda=agenda,
		recomendaciones=[],
		datos_normalizados={"labs": [l.model_dump() for l in paciente.labs]},
		puntuacion_metas={
			"programa": programa,
			"puntaje": puntaje,
			"riesgo_categoria": riesgo_cat,
			"metas_incumplidas": [m for m in [
				"LDL por encima de objetivo" if any(l.nombre == "COLESTEROL LDL" and l.valor >= 130 for l in paciente.labs) else None,
				"HbA1c por encima de objetivo" if any(l.nombre == "HEMOGLOBINA GLICOSILADA (HBA1C)" and l.valor >= 7 for l in paciente.labs) else None,
				"Presión arterial sistólica elevada" if any(l.nombre == "PRESION ARTERIAL SISTOLICA" and l.valor >= 140 for l in paciente.labs) else None,
			] if m],
			"metas_cumplidas": [m for m in [
				"Creatinina monitorizada" if any(l.nombre == "CREATININA EN SUERO U OTROS" for l in paciente.labs) else None,
				"Función renal evaluada (CrCl)" if crcl is not None else None,
			] if m],
		},
		riesgo_cv={
			"categoria": riesgo_cat,
			"puntaje": puntaje,
			"ascvd": resumen_riesgo.ascvd,
			"justificacion": justificacion_riesgo,
		},
		alertas_tfg=[a for a in [
			"Aclaramiento reducido: considerar ajuste por función renal" if (crcl is not None and crcl < 60) else None,
			"Posible progresión ERC: confirmar estadio" if (paciente.estadio_erc and paciente.estadio_erc >= 3) else None,
		] if a],
	)

__all__ = ["analizar_paciente"]
