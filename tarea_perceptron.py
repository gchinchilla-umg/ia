import numpy as np
import matplotlib.pyplot as plt

# ─────────────────────────────────────────
#  1. DEFINICIÓN DEL PERCEPTRÓN
# ─────────────────────────────────────────

class PerceptronCredito:
    def __init__(self, entradas, pesos, sesgo=0):
        self.entradas = np.array(entradas, dtype=float)
        self.pesos    = np.array(pesos,    dtype=float)
        self.sesgo    = sesgo

    # ── Función de activación ──────────────
    @staticmethod
    def sigmoide(z):
        return 1 / (1 + np.exp(-z))

    # ── Propagación hacia adelante ─────────
    def forward(self):
        self.z = np.dot(self.pesos, self.entradas) + self.sesgo
        self.probabilidad = self.sigmoide(self.z)
        self.decision = 1 if self.probabilidad >= 0.5 else 0
        return self.decision

    # ── Reporte en consola ─────────────────
    def mostrar_resultado(self):
        print("=" * 50)
        print("     SISTEMA DE APROBACIÓN DE CRÉDITO")
        print("=" * 50)
        print(f"Ingresos altos        : {int(self.entradas[0])}")
        print(f"Historial bueno       : {int(self.entradas[1])}")
        print(f"Empleo estable        : {int(self.entradas[2])}")
        print("-" * 50)
        print(f"Suma ponderada (z)    : {self.z:.4f}")
        print(f"Probabilidad σ(z)     : {self.probabilidad:.4f}")
        print("-" * 50)

        if self.decision == 1:
            print("✅ CRÉDITO APROBADO")
        else:
            print("❌ CRÉDITO RECHAZADO")
        print("=" * 50)


# ─────────────────────────────────────────
#  2. DATOS DEL CASO
# ─────────────────────────────────────────
# 1 = Sí cumple condición
# 0 = No cumple condición

entradas = [1, 1, 0]   # Tiene ingresos y buen historial, pero no empleo estable

# Pesos (importancia de cada criterio)
pesos = [1.0, 1.2, 0.8]

# Bias ajustado para exigir al menos 2 condiciones fuertes
sesgo = -1.5


# ─────────────────────────────────────────
#  3. EJECUCIÓN
# ─────────────────────────────────────────

modelo = PerceptronCredito(entradas, pesos, sesgo)
modelo.forward()
modelo.mostrar_resultado()


# ─────────────────────────────────────────
#  4. VISUALIZACIÓN DE LA SIGMOIDE
# ─────────────────────────────────────────

z_vals = np.linspace(-6, 6, 300)
s_vals = PerceptronCredito.sigmoide(z_vals)

plt.figure(figsize=(8, 4))
plt.plot(z_vals, s_vals, linewidth=2.5, label='σ(z)')

z_punto = modelo.z
s_punto = modelo.probabilidad

plt.scatter(z_punto, s_punto, s=100)
plt.axvline(z_punto, linestyle='--', alpha=0.4)
plt.axhline(s_punto, linestyle='--', alpha=0.4)

plt.title('Probabilidad de Aprobación — Modelo de Crédito')
plt.xlabel('z (Evaluación financiera)')
plt.ylabel('Probabilidad de aprobación')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()