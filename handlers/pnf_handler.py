# handlers/pnf_handler.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import os


# DICCIONARIO MAESTRO CON TODOS LOS PNF (TODOS LOS NÚCLEOS)

PNF_DATA = {
    "administracion": {
        "nombre": "Administración",
        "botones": [
            ("📝 Asistente Administrativo (Trayecto I)", "asistente"),
            ("🧑‍💼 TSU en Administración (Trayecto II)", "tsu"),
            ("🎓 Licenciado en Administración (Trayecto IV)", "licenciado"),
            ("📄 Documento Rector PNF", "documento_rector")  # Nuevo botón
        ],
        "textos": {
            "asistente": (
                "<b>📝 PERFIL DEL EGRESADO: ASISTENTE ADMINISTRATIVO</b>\n\n"
                "• Desarrolla capacidades operativas para brindar apoyo directo en la ejecución y seguimiento de los procesos administrativos cotidianos.\n"
                "• Participa en la recolección, organización, actualización y registro de información contable, financiera y de gestión de talento humano.\n"
                "• Aplica herramientas ofimáticas y tecnologías de información para agilizar las tareas de oficina y mejorar la calidad de atención dentro de las organizaciones."
            ),
            "tsu": (
                "<b>🧑‍💼 PERFIL DEL EGRESADO: TSU EN ADMINISTRACIÓN</b>\n\n"
                "• Participa activamente en la transformación de su entorno laboral y sociocomunitario mediante la supervisión y conducción técnica de los procesos administrativos.\n"
                "• Formula propuestas y contribuye a la puesta en práctica de acciones operativas en las fases de planificación, organización, dirección y control.\n"
                "• Aplica técnicas y procedimientos administrativos, contables y financieros, garantizando que se cumplan de acuerdo al marco legal vigente.\n"
                "• Detecta y soluciona problemas de nivel intermedio, apoyándose en el trabajo en equipo y métodos básicos de investigación para optimizar el funcionamiento organizacional."
            ),
            "licenciado": (
                "<b>🎓 PERFIL DEL EGRESADO: LICENCIADO EN ADMINISTRACIÓN</b>\n\n"
                "• Es un profesional integral con visión estratégica que planifica, organiza, dirige, controla y evalúa procesos gerenciales y sistemas administrativos complejos.\n"
                "• Analiza y soluciona problemas estructurales en áreas clave como talento humano, finanzas, logística y operaciones en distintos tipos de instituciones (públicas, privadas o de propiedad social).\n"
                "• Diseña, innova y desarrolla nuevos modelos administrativos que impulsan la transformación productiva y rompen con la burocracia tradicional.\n"
                "• Ejerce el liderazgo desde un enfoque humanista, crítico y dialéctico, integrándose con conciencia al desarrollo socioeconómico, político, sustentable y sostenible del país."
            )
        }
    },
    "construccion": {
        "nombre": "Construcción Civil",
        "botones": [
            ("🗺️ Asistente en Topografía (Trayecto I)", "topografia"),
            ("✏️ Dibujante Técnico (Trayecto I)", "dibujante"),
            ("📐 TSU en Construcción Civil", "tsu"),
            ("🏗️ Ingeniero en Construcción Civil", "ingeniero"),
            ("📄 Documento Rector PNF", "documento_rector")  # Nuevo botón
        ],
        "textos": {
            "topografia": (
                "<b>🗺️ CERTIFICACIÓN: ASISTENTE EN TOPOGRAFÍA</b>\n\n"
                "Capacitado para apoyar en levantamientos topográficos, manejo de equipos básicos y procesamiento de datos de campo."
            ),
            "dibujante": (
                "<b>✏️ CERTIFICACIÓN: DIBUJANTE TÉCNICO DE OBRAS CIVILES</b>\n\n"
                "Competencias en dibujo asistido por computadora (CAD), interpretación de planos y elaboración de detalles constructivos."
            ),
            "tsu": (
                "<b>📐 PERFIL DEL EGRESADO: TSU EN CONSTRUCCIÓN CIVIL</b>\n\n"
                "Profesional íntegro con pensamiento crítico, innovador y emprendedor.\n\n"
                "• Lee e interpreta planos de proyectos civiles.\n"
                "• Realiza planes de construcción (etapas, mano de obra, materiales).\n"
                "• Ejecuta ensayos de laboratorio y control de calidad.\n"
                "• Inspecciona obras (edificaciones, vialidad, sistemas hidrosanitarios).\n"
                "• Elabora estructuras de costo y administración de obras."
            ),
            "ingeniero": (
                "<b>🏗️ PERFIL DEL EGRESADO: INGENIERO EN CONSTRUCCIÓN CIVIL</b>\n\n"
                "Profesional con pensamiento creativo, científico e innovador, alta conciencia social.\n\n"
                "• Diagnostica, planea, diseña, gestiona y construye soluciones integrales para edificaciones, infraestructura vial y servicios básicos.\n"
                "• Desarrolla proyectos urbanos y rurales.\n"
                "• Construye modelos y simulaciones con nuevas tecnologías.\n"
                "• Gestiona el aprovechamiento racional de recursos naturales."
            )
        }
    },
    "contaduria": {
        "nombre": "Contaduría Pública",
        "botones": [
            ("📊 Asistente Contable (Trayecto I)", "asistente"),
            ("🧮 TSU en Contaduría Pública (Trayecto II)", "tsu"),
            ("🎓 Licenciado en Contaduría Pública (Trayecto IV)", "licenciado"),
            ("📜 Postgrados", "postgrado"),
            ("📄 Documento Rector PNF", "documento_rector")  # Nuevo botón
        ],
        "textos": {
            "asistente": (
                "<b>📊 CERTIFICADO DE ASISTENTE CONTABLE</b>\n\n"
                "Este nivel se obtiene al aprobar satisfactoriamente el <b>Trayecto Inicial</b> (12 semanas) y el <b>Trayecto I</b> del programa."
            ),
            "tsu": (
                "<b>🧮 PERFIL DEL EGRESADO: TSU EN CONTADURÍA PÚBLICA</b>\n\n"
                "El TSU en Contaduría Pública es un profesional capacitado para llevar registros contables, elaborar estados financieros básicos y aplicar normas tributarias y laborales bajo supervisión, con ética y responsabilidad.\n\n"
                "• Maneja sistemas de información contable.\n"
                "• Prepara declaraciones de impuestos básicas.\n"
                "• Asiste en auditorías internas.\n"
                "• Aplica principios de contabilidad generalmente aceptados."
            ),
            "licenciado": (
                "<b>🎓 PERFIL DEL EGRESADO: LICENCIADO EN CONTADURÍA PÚBLICA</b>\n\n"
                "Profesional integral con capacidad para diseñar, implementar y evaluar sistemas contables, financieros y de control en organizaciones públicas y privadas.\n\n"
                "• Gestiona la información financiera para la toma de decisiones.\n"
                "• Realiza auditorías externas e internas.\n"
                "• Asesora en materia fiscal, societaria y de costos.\n"
                "• Participa en la formulación de proyectos de inversión y presupuestos."
            ),
            "postgrado": (
                "<b>📜 POSTGRADOS EN CONTADURÍA PÚBLICA</b>\n\n"
                "Una vez obtenido el título de <b>Licenciado(a) en Contaduría Pública</b>, el profesional puede continuar su formación en:\n\n"
                "• <b>Especialización</b> (1 año)\n"
                "• <b>Maestría en Ciencias Contables</b> (requiere Especialista, 2 años)\n"
                "• <b>Doctorado en Ciencias Contables</b> (requiere Maestría, 4 años)"
            )
        }
    },
    "electricidad": {
        "nombre": "Electricidad",
        "botones": [
            ("🛠️ Electricista I (Trayecto I)", "electricista1"),
            ("⚙️ Tecnólogo Electricista (Trayecto III)", "tecnologo"),
            ("🔌 TSU en Electricidad", "tsu"),
            ("🚀 Ingeniero Electricista", "ingeniero"),
            ("📄 Documento Rector PNF", "documento_rector")  # Nuevo botón
        ],
        "textos": {
            "electricista1": (
                "<b>🛠️ CERTIFICACIÓN: ELECTRICISTA I</b>\n\n"
                "Capacitado para realizar instalaciones eléctricas básicas, mantenimiento de circuitos residenciales y comerciales pequeños, aplicando normas de seguridad."
            ),
            "tecnologo": (
                "<b>⚙️ CERTIFICACIÓN: TECNÓLOGO ELECTRICISTA</b>\n\n"
                "Competencias intermedias: supervisión de instalaciones, diagnóstico de fallas en sistemas eléctricos industriales, y manejo de equipos de medición avanzados."
            ),
            "tsu": (
                "<b>🔌 PERFIL DEL EGRESADO: TSU EN ELECTRICIDAD</b>\n\n"
                "Profesional con pensamiento crítico, científico y humanista.\n\n"
                "• Lee e interpreta planos eléctricos, selecciona equipos.\n"
                "• Diagnostica y corrige averías, elabora informes técnicos.\n"
                "• Organiza mantenimiento sistemático.\n"
                "• Controla materiales y personal, aplica normas de seguridad.\n"
                "• Participa en estudios de carga, flujo de potencia, cortocircuito y diseño de iluminación.\n"
                "• Propone soluciones para uso eficiente de energía en comunidades."
            ),
            "ingeniero": (
                "<b>🚀 PERFIL DEL EGRESADO: INGENIERO ELECTRICISTA</b>\n\n"
                "Profesional con conocimientos avanzados para planificación, diseño, evaluación, innovación y gestión de proyectos en sistemas eléctricos.\n\n"
                "• Realiza estudios de flujo de carga, estabilidad, cortocircuito y despacho económico.\n"
                "• Aplica normas nacionales e internacionales, criterios de eficiencia energética.\n"
                "• Dirige planes de mantenimiento y gestiona centros de despacho de carga.\n"
                "• Analiza calidad de la energía y valida prototipos.\n"
                "• Investiga nuevas tecnologías y promueve energías alternativas."
            )
        }
    },
    "industrial": {
        "nombre": "Ingeniería Industrial",
        "botones": [
            ("⚙️ TSU en Producción Industrial", "tsu"),
            ("🏭 Ingeniero Industrial", "ingeniero"),
            ("📄 Documento Rector PNF", "documento_rector")  # Nuevo botón
        ],
        "textos": {
            "tsu": (
                "<b>⚙️ PERFIL DEL EGRESADO: TSU EN PRODUCCIÓN INDUSTRIAL</b>\n\n"
                "El profesional T.S.U. en Producción Industrial egresado de este programa es capaz de resolver problemáticas en el campo industrial que afecten la productividad.\n\n"
                "<b>Competencias:</b>\n"
                "• <b>Gestión y Logística:</b> Administra la cadena de suministro mediante sistemas de logística.\n"
                "• <b>Manufactura y Calidad:</b> Gestiona procesos de manufactura utilizando técnicas de administración de operaciones y aseguramiento de la calidad.\n"
                "• <b>Supervisión:</b> Supervisa líneas de producción, asigna operaciones, realiza estudios de tiempo y movimiento.\n"
                "• <b>Administración Técnica:</b> Elabora presupuestos de manufactura, maneja sistemas de información, expedientes técnicos y formularios para auditorías industriales."
            ),
            "ingeniero": (
                "<b>🏭 PERFIL DEL EGRESADO: INGENIERO INDUSTRIAL</b>\n\n"
                "El Ingeniero Industrial egresado es un profesional humanista, creativo, dinámico y seguro, con capacidad para liderar el cambio y buscar el mejoramiento continuo.\n\n"
                "<b>Competencias:</b>\n"
                "• <b>Estrategia y Optimización:</b> Diseña e implementa estrategias para alcanzar la máxima competitividad y productividad.\n"
                "• <b>Gestión Integral:</b> Planifica, supervisa y controla procesos industriales, incluyendo aspectos económicos, financieros, administrativos y talento humano.\n"
                "• <b>Seguridad y Ambiente:</b> Diseña planes de seguridad e higiene laboral.\n"
                "• <b>Desarrollo Sustentable:</b> Planifica plantas industriales con tecnologías limpias.\n"
                "• <b>Análisis Crítico:</b> Aplica análisis críticos, situacionales y estadísticos.\n"
                "• <b>Prevención de Riesgos:</b> Evalúa e implementa estrategias para prevenir riesgos operativos."
            )
        }
    },
    "informatica": {
        "nombre": "Informática",
        "botones": [
            ("🏆 Titulaciones y Certificaciones", "info"),
            ("🧑‍💻 Perfil TSU en Informática", "tsu"),
            ("🚀 Perfil Ingeniero en Informática", "ing"),
            ("📄 Documento Rector PNF", "documento_rector")  # Nuevo botón
        ],
        "textos": {
            "info": (
                "<b>🏆 TITULACIONES Y CERTIFICACIONES - INFORMÁTICA</b>\n\n"
                "<b>🏆 Títulos Universitarios:</b>\n"
                "• 🧑‍💻 Trayecto II: TSU en Informática.\n"
                "• 🚀 Trayecto IV: Ingeniero(a) en Informática.\n"
                "• 📜 Postgrados: Especializaciones, Maestrías y Doctorados.\n\n"
                "<b>🛠️ Certificaciones Intermedias:</b>\n"
                "• 🔧 Trayecto I: Soporte Técnico a Usuarios y Equipos.\n"
                "• 💻 Trayecto III: Desarrollador de Aplicaciones.\n\n"
                "📌 <i>Las certificaciones avalan destrezas prácticas antes de la titulación final.</i>"
            ),
            "tsu": (
                "<b>🧑‍💻 PERFIL DEL EGRESADO: TSU EN INFORMÁTICA</b>\n\n"
                "Es un profesional integral capacitado para resolver problemas técnicos operativos, desarrollar software a menor escala con altos estándares de calidad y aplicar la tecnología con ética y responsabilidad social.\n\n"
                "<b>🛠️ Competencias y Habilidades Clave:</b>\n"
                "• 💻 <b>Desarrollo de Software</b>: Construye y mantiene componentes de software de calidad, priorizando siempre el uso de <b>Software Libre</b>.\n"
                "• 🔧 <b>Soporte de Hardware</b>: Ensambla y realiza el mantenimiento preventivo y correctivo de equipos informáticos.\n"
                "• 📊 <b>Bases de Datos</b>: Interpreta modelos de datos y se encarga de mantener operativas y eficientes las bases de datos.\n"
                "• 🌐 <b>Conectividad</b>: Instala y configura redes de área local (LAN).\n"
                "• ⚙️ <b>Evaluación Técnica</b>: Participa de forma técnica en los procesos de evaluación e instalación de nuevos softwares.\n\n"
                "<i>🌱 Todo su desempeño se realiza en armonía con la preservación del ambiente y el progreso socio-productivo de su entorno.</i>"
            ),
            "ing": (
                "<b>🚀 PERFIL DEL EGRESADO: INGENIERO EN INFORMÁTICA</b>\n\n"
                "Es un profesional líder con formación integral para analizar, desarrollar e implementar sistemas informáticos de alta calidad. Está orientado a optimizar la gestión de la Administración Pública Nacional, organizaciones y comunidades, siendo un protagonista activo de la Soberanía Tecnológica del país.\n\n"
                "<b>🛠️ Competencias y Habilidades Avanzadas:</b>\n"
                "• 💼 <b>Gestión y Auditoría</b>: Administra proyectos informáticos de gran alcance y audita sistemas para garantizar su correcto funcionamiento y seguridad.\n"
                "• 💻 <b>Desarrollo e Integración</b>: Desarrolla, implementa de forma masiva e integra diversos sistemas informáticos, priorizando el uso de plataformas libres.\n"
                "• 📊 <b>Diseño de Datos</b>: Diseña y estructura bases de datos complejas.\n"
                "• 🌐 <b>Conectividad de Alto Nivel</b>: Diseña redes informáticas bajo estándares de calidad.\n"
                "• 🔍 <b>Investigación y Comunidad</b>: Investiga activamente para resolver problemas sociales mediante las TIC.\n\n"
                "<i>🌱 Un profesional con capacidad emprendedora, ético y comprometido con la transformación social.</i>"
            )
        }
    },
    "mantenimiento": {
        "nombre": "Ingeniería de Mantenimiento",
        "botones": [
            ("🔧 Asistente en Mantenimiento (Trayecto I)", "asistente"),
            ("🛠️ TSU en Mantenimiento (Trayecto II)", "tsu"),
            ("📊 Supervisor en Mantenimiento (Trayecto III)", "supervisor"),
            ("🚀 Ingeniero en Mantenimiento (Trayecto IV)", "ingeniero"),
            ("📄 Documento Rector PNF", "documento_rector")  # Nuevo botón
        ],
        "textos": {
            "asistente": (
                "<b>🔧 PERFIL: ASISTENTE EN MANTENIMIENTO (Trayecto I)</b>\n\n"
                "Capacitado para ejecutar rutinas básicas e instrucciones directas en la preservación de equipos e instalaciones.\n\n"
                "<b>Competencias principales:</b>\n"
                "• Manejo adecuado de herramientas mecánicas, eléctricas e instrumentos de medición.\n"
                "• Lectura e interpretación de manuales de fabricantes y planos técnicos.\n"
                "• Ejecución de órdenes de trabajo en mantenimiento preventivo y correctivo menor.\n"
                "• Aplicación de normas básicas de higiene, seguridad industrial y ambiente."
            ),
            "tsu": (
                "<b>🛠️ PERFIL: TSU EN MANTENIMIENTO (Trayecto II)</b>\n\n"
                "Profesional capacitado para la supervisión operativa, ejecución autónoma y planificación a corto plazo de los planes de mantenimiento.\n\n"
                "<b>Competencias principales:</b>\n"
                "• Supervisión, dirección y control de cuadrillas.\n"
                "• Programación y ejecución técnica de planes de mantenimiento preventivo, predictivo y correctivo.\n"
                "• Control básico de inventarios y gestión de repuestos.\n"
                "• Diagnóstico de fallas operativas recurrentes.\n"
                "• Levantamiento de historiales de máquinas y elaboración de informes técnicos."
            ),
            "supervisor": (
                "<b>📊 PERFIL: SUPERVISOR EN ADMINISTRACIÓN Y EJECUCIÓN DEL MANTENIMIENTO (Trayecto III)</b>\n\n"
                "Orientado a la coordinación táctica, la administración eficiente de los recursos y la optimización de los procesos a mediano plazo.\n\n"
                "<b>Competencias principales:</b>\n"
                "• Cálculo y seguimiento de indicadores de gestión (Disponibilidad, Confiabilidad, Mantenibilidad).\n"
                "• Coordinación de recursos humanos, materiales y financieros, incluyendo planificación de paradas de planta.\n"
                "• Implementación de técnicas de mantenimiento predictivo (vibraciones, termografía, etc.).\n"
                "• Análisis de fallas complejas (Análisis Causa-Raíz).\n"
                "• Administración de sistemas computarizados para gestión del mantenimiento (CMMS)."
            ),
            "ingeniero": (
                "<b>🚀 PERFIL: INGENIERO EN MANTENIMIENTO (Trayecto IV)</b>\n\n"
                "Profesional integral con capacidad gerencial, estratégica y de diseño para liderar la gestión de activos y la ingeniería de confiabilidad.\n\n"
                "<b>Competencias principales:</b>\n"
                "• Diseño e implementación de políticas de mantenimiento estratégico.\n"
                "• Aplicación de metodologías avanzadas (RCM, TPM).\n"
                "• Auditoría de sistemas y evaluación del ciclo de vida de activos.\n"
                "• Toma de decisiones basadas en análisis de riesgo y factibilidad económica.\n"
                "• Desarrollo de proyectos de innovación para resolver problemas estructurales de la industria."
            )
        }
    },
    "mecanica": {
        "nombre": "Mecánica",
        "botones": [
            ("⚙️ TSU en Mecánica", "tsu"),
            ("🔩 Ingeniero Mecánico", "ingeniero"),
            ("📄 Documento Rector PNF", "documento_rector")  # Nuevo botón
        ],
        "textos": {
            "tsu": (
                "<b>⚙️ PERFIL DEL EGRESADO: TSU EN MECÁNICA</b>\n\n"
                "• <b>Gestión Operativa:</b> Ejecuta, supervisa y controla procesos de manufactura, instalación y mantenimiento de equipos mecánicos.\n"
                "• <b>Solución de Problemas:</b> Detecta fallas operativas y aplica soluciones técnicas inmediatas.\n"
                "• <b>Participación en Equipos:</b> Colabora en proyectos socioproductivos.\n"
                "• <b>Respeto Normativo:</b> Aplica normativas legales, ambientales y de seguridad industrial."
            ),
            "ingeniero": (
                "<b>🔩 PERFIL DEL EGRESADO: INGENIERO MECÁNICO</b>\n\n"
                "• <b>Gestión Estratégica:</b> Diseña, planifica y dirige sistemas mecánicos complejos y procesos de gestión de activos.\n"
                "• <b>Innovación Tecnológica:</b> Desarrolla capacidades para innovación y adaptación de nuevas tecnologías.\n"
                "• <b>Liderazgo Multidisciplinario:</b> Coordina proyectos de investigación y desarrollo.\n"
                "• <b>Compromiso Social y Ético:</b> Contribuye al desarrollo endógeno sustentable."
            )
        }
    },
    "psicologia": {
        "nombre": "Psicología Social",
        "botones": [
            ("🎓 Perfil del Licenciado en Psicología Social", "licenciado"),
            ("📄 Documento Rector PNF", "documento_rector")  # Nuevo botón
        ],
        "textos": {
            "licenciado": (
                "<b>🧠 PERFIL DEL EGRESADO: PSICÓLOGO SOCIAL</b>\n\n"
                "El perfil se fundamenta en cuatro ejes de saber:\n\n"
                "<b>1. SABER CONOCER</b>\n"
                "• Conocimiento profundo de problemas sociales y culturales.\n"
                "• Comprensión de procesos psicosociales (dinámica de grupos, influencia social).\n"
                "• Manejo de imaginarios sociales y metodología cuali-cualitativa.\n\n"
                "<b>2. SABER HACER</b>\n"
                "• Diseñar, ejecutar y evaluar proyectos socioproductivos e intervenciones psicosociales.\n"
                "• Liderar procesos de cambio grupales, comunitarios e institucionales.\n"
                "• Utilizar software especializado para análisis de datos.\n"
                "• Detectar y manejar conflictos sociales.\n\n"
                "<b>3. SABER SER</b>\n"
                "• Responsabilidad, compromiso social y ética profesional.\n"
                "• Respeto a los derechos, dignidad y diferencias.\n"
                "• Compromiso con el bienestar y aprendizaje permanente.\n\n"
                "<b>4. SABER CONVIVIR</b>\n"
                "• Actuar responsablemente en contextos comunitarios e institucionales.\n"
                "• Evaluar proyectos de intervención y mediar en conflictos.\n"
                "• Coordinar esfuerzos de integración grupal."
            )
        }
    },
    "turismo": {
        "nombre": "Turismo",
        "botones": [
            ("🎒 TSU en Turismo", "tsu"),
            ("🎓 Licenciado en Turismo", "licenciado"),
            ("📄 Documento Rector PNF", "documento_rector")  # Nuevo botón
        ],
        "textos": {
            "tsu": (
                "<b>🎒 PERFIL DEL EGRESADO: TSU EN TURISMO</b>\n\n"
                "• Competencias operativas: agente de turismo, asesoría, supervisión hotelera.\n"
                "• Enfoque de trabajo flexible y dinámico (Ser, Conocer, Hacer, Convivir, Emprender).\n"
                "• Vinculación social: solución de problemas del entorno."
            ),
            "licenciado": (
                "<b>🎓 PERFIL DEL EGRESADO: LICENCIADO EN TURISMO (Menciones)</b>\n\n"
                "Profesional integral con cuatro menciones:\n\n"
                "• <b>Guiatura de Turismo</b>: interpretación del patrimonio.\n"
                "• <b>Alojamiento</b>: gestión de la hospitalidad.\n"
                "• <b>Gastronomía</b>: rescate de productos autóctonos.\n"
                "• <b>Gestión Turística</b>: planificación con enfoque social.\n\n"
                "<i>El estudiante elige una mención para profundizar.</i>"
            )
        }
    }
}


# TEXTOS DE CONTEXTO PARA LOS MENÚS DE PNF


TEXTO_CONTEXTO_LISTADO_PNF = (
    "<b>📚 Programas Nacionales de Formación (PNF)</b>\n\n"
    "Los PNF son los programas de pregrado que ofrece la UPTTMBI. "
    "En esta sección podrás consultar información detallada sobre cada carrera:\n"
    "• Titulaciones y certificaciones\n"
    "• Perfiles de egreso (TSU, Ingeniero, Licenciado)\n"
    "• Competencias y áreas de desempeño\n\n"
    "⬇️ <b>Selecciona una carrera para ver su información detallada:</b>"
)

TEXTO_CONTEXTO_SUBMENU_PNF = (
    "<b>📘 {nombre_carrera}</b>\n\n"
    "Aquí encontrarás los distintos niveles de formación y certificaciones "
    "que ofrece este PNF. Selecciona la opción que te interese para ver "
    "el perfil completo del egresado.\n\n"
    "⬇️ <b>Opciones disponibles:</b>"
)

# Mapeo de claves de PNF a nombre de archivo y título del documento
DOCUMENTOS_RECTOR = {
    "administracion": {
        "archivo": "DOCUMENTO_RECTOR_PNFA.pdf",
        "titulo": "Administración",
        "descripcion": "Documento Rector del PNF en Administración. Establece las bases, objetivos y estructura del programa."
    },
    "construccion": {
        "archivo": "DOCUMENTO_RECTOR_PNFCC.pdf",
        "titulo": "Construcción Civil",
        "descripcion": "Documento Rector del PNF en Construcción Civil. Establece las bases, objetivos y estructura del programa."
    },
    "contaduria": {
        "archivo": "DOCUMENTO_RECTOR_PNFCP.pdf",
        "titulo": "Contaduría Pública",
        "descripcion": "Documento Rector del PNF en Contaduría Pública. Establece las bases, objetivos y estructura del programa."
    },
    "electricidad": {
        "archivo": "DOCUMENTO_RECTOR_PNFE.pdf",
        "titulo": "Electricidad",
        "descripcion": "Documento Rector del PNF en Electricidad. Establece las bases, objetivos y estructura del programa."
    },
    "industrial": {
        "archivo": "DOCUMENTO_RECTOR_PNFIInd.pdf",
        "titulo": "Ingeniería Industrial",
        "descripcion": "Documento Rector del PNF en Ingeniería Industrial. Establece las bases, objetivos y estructura del programa."
    },
    "informatica": {
        "archivo": "DOCUMENTO_RECTOR_PNFI.pdf",
        "titulo": "Informática",
        "descripcion": "Documento Rector del PNF en Informática. Establece las bases, objetivos y estructura del programa."
    },
    "mantenimiento": {
        "archivo": "DOCUMENTO_RECTOR_PNFMTO.pdf",
        "titulo": "Ingeniería de Mantenimiento",
        "descripcion": "Documento Rector del PNF en Ingeniería de Mantenimiento. Establece las bases, objetivos y estructura del programa."
    },
    "mecanica": {
        "archivo": "DOCUMENTO_RECTOR_PNFM.pdf",
        "titulo": "Mecánica",
        "descripcion": "Documento Rector del PNF en Mecánica. Establece las bases, objetivos y estructura del programa."
    },
    "psicologia": {
        "archivo": "DOCUMENTO_RECTOR_PNFPS.pdf",
        "titulo": "Psicología Social",
        "descripcion": "Documento Rector del PNF en Psicología Social. Establece las bases, objetivos y estructura del programa."
    },
    "turismo": {
        "archivo": "DOCUMENTO_RECTOR_PNFT.pdf",
        "titulo": "Turismo",
        "descripcion": "Documento Rector del PNF en Turismo. Establece las bases, objetivos y estructura del programa."
    }
}


# FUNCIONES AUXILIARES (navegación normal con edit_message_text)

async def mostrar_listado_pnf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el menú principal con todos los PNF (edita el mensaje original)."""
    query = update.callback_query
    await query.answer()

    items = sorted(PNF_DATA.items(), key=lambda x: x[1]["nombre"])
    keyboard = []
    fila = []
    for key, data in items:
        fila.append(InlineKeyboardButton(data["nombre"], callback_data=f"pnf_detalle_{key}"))
        if len(fila) == 2:
            keyboard.append(fila)
            fila = []
    if fila:
        keyboard.append(fila)

    keyboard.append([InlineKeyboardButton("⬅️ Volver a Institucional", callback_data='institucional_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        TEXTO_CONTEXTO_LISTADO_PNF,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def mostrar_submenu_pnf(update: Update, context: ContextTypes.DEFAULT_TYPE, pnf_key: str):
    """Muestra el submenú de un PNF (edita el mensaje original)."""
    query = update.callback_query
    data = PNF_DATA.get(pnf_key)
    if not data:
        await query.edit_message_text("❌ PNF no encontrado.")
        return

    keyboard = []
    for texto, callback_key in data["botones"]:
        keyboard.append([InlineKeyboardButton(texto, callback_data=f"pnf_perfil_{pnf_key}_{callback_key}")])
    keyboard.append([InlineKeyboardButton("⬅️ Volver al listado PNF", callback_data='pnf_listado')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    texto_contexto = TEXTO_CONTEXTO_SUBMENU_PNF.format(nombre_carrera=data['nombre'])
    await query.edit_message_text(
        texto_contexto,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


# FUNCIONES PARA ENVIAR MENÚS COMO MENSAJES NUEVOS (después de una acción)

async def mostrar_submenu_pnf_nuevo(chat_id, context, pnf_key):
    """Envía un mensaje NUEVO con el submenú del PNF y registra su ID."""
    data = PNF_DATA.get(pnf_key)
    if not data:
        await context.bot.send_message(chat_id=chat_id, text="❌ PNF no encontrado.")
        return

    keyboard = []
    for texto, callback_key in data["botones"]:
        keyboard.append([InlineKeyboardButton(texto, callback_data=f"pnf_perfil_{pnf_key}_{callback_key}")])
    keyboard.append([InlineKeyboardButton("⬅️ Volver al listado PNF", callback_data='pnf_listado')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    texto_contexto = TEXTO_CONTEXTO_SUBMENU_PNF.format(nombre_carrera=data['nombre'])
    new_msg = await context.bot.send_message(
        chat_id=chat_id,
        text=texto_contexto,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    context.user_data.setdefault('menu_messages', []).append(new_msg.message_id)


# MANEJADOR DE PERFILES (envía el texto del perfil sin botones, luego el submenú)

async def mostrar_perfil_pnf(update: Update, context: ContextTypes.DEFAULT_TYPE, pnf_key: str, perfil_key: str):
    """Muestra el texto de un perfil como mensaje nuevo (sin botones), luego vuelve a mostrar el submenú.
       Si perfil_key es 'documento_rector', envía el PDF correspondiente."""
    query = update.callback_query
    chat_id = query.message.chat_id

    # 1. Eliminar el menú actual
    try:
        await query.message.delete()
    except:
        pass

    # 2. Borrar todos los mensajes de menú anteriores registrados
    if 'menu_messages' in context.user_data:
        for msg_id in context.user_data['menu_messages']:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except:
                pass
        context.user_data['menu_messages'] = []

    # 3. Caso especial: enviar documento rector
    if perfil_key == "documento_rector":
        doc_info = DOCUMENTOS_RECTOR.get(pnf_key)
        if not doc_info:
            await context.bot.send_message(chat_id=chat_id, text="❌ Documento rector no definido para este PNF.")
        else:
            # Enviar mensaje temporal
            temp_msg = await context.bot.send_message(chat_id=chat_id, text="📄 Enviando Documento Rector, por favor espera...")
            ruta_pdf = os.path.join("assets", "pnf", doc_info["archivo"])
            try:
                if os.path.exists(ruta_pdf):
                    with open(ruta_pdf, 'rb') as pdf:
                        await context.bot.send_document(
                            chat_id=chat_id,
                            document=pdf,
                            caption=f"📘 Documento Rector del PNF en {doc_info['titulo']}\n\n{doc_info['descripcion']}"
                        )
                else:
                    await context.bot.send_message(chat_id=chat_id, text=f"❌ El documento rector para {doc_info['titulo']} no está disponible temporalmente.")
            except Exception:
                pass
            finally:
                try:
                    await temp_msg.delete()
                except:
                    pass
        # Mostrar el submenú de nuevo
        await mostrar_submenu_pnf_nuevo(chat_id, context, pnf_key)
        return

    # 4. Comportamiento normal para perfiles de texto
    data = PNF_DATA.get(pnf_key)
    texto = data["textos"].get(perfil_key, "❌ Información no disponible temporalmente.") if data else "❌ PNF no encontrado."

    await context.bot.send_message(
        chat_id=chat_id,
        text=texto,
        parse_mode='HTML'
    )

    await mostrar_submenu_pnf_nuevo(chat_id, context, pnf_key)

# MANEJADORES PRINCIPALES PARA EL ROUTER

async def manejar_pnf_seleccion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    pnf_key = data.replace("pnf_detalle_", "")
    await mostrar_submenu_pnf(update, context, pnf_key)

async def manejar_perfil_pnf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    parts = data.split("_")
    if len(parts) >= 4:
        pnf_key = parts[2]
        perfil_key = "_".join(parts[3:])
        await mostrar_perfil_pnf(update, context, pnf_key, perfil_key)
    else:
        await query.message.reply_text("❌ Formato de callback incorrecto.")

async def manejar_menu_pnf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    pnf_key = data.replace("pnf_menu_", "")
    chat_id = query.message.chat_id

    try:
        await query.message.delete()
    except:
        pass

    if 'menu_messages' in context.user_data:
        for msg_id in context.user_data['menu_messages']:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except:
                pass
        context.user_data['menu_messages'] = []

    await mostrar_submenu_pnf_nuevo(chat_id, context, pnf_key)