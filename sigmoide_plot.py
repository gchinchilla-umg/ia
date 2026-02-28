import numpy as np
import matplotlib.pyplot as plt

# ─────────────────────────────────────────
#  1. DEFINICIÓN DEL PERCEPTRÓN
# ─────────────────────────────────────────

class Perceptron:
    def __init__(self, entradas, pesos, sesgo=0):
        """
        entradas : lista de valores de entrada
        pesos    : lista de pesos sinápticos
        sesgo    : bias (por defecto 0)
        """
        self.entradas = np.array(entradas, dtype=float)
        self.pesos    = np.array(pesos,    dtype=float)
        self.sesgo    = sesgo

    # ── Función de activación ──────────────
    @staticmethod
    def sigmoide(z):
        return 1 / (1 + np.exp(-z))

    @staticmethod
    def sigmoide_derivada(z):
        s = Perceptron.sigmoide(z)
        return s * (1 - s)

    # ── Propagación hacia adelante ─────────
    def forward(self):
        self.z      = np.dot(self.pesos, self.entradas) + self.sesgo
        self.salida = self.sigmoide(self.z)
        return self.salida

    # ── Reporte en consola ─────────────────
    def mostrar_resultado(self):
        print("=" * 45)
        print("       PERCEPTRÓN SIMPLE — SIGMOIDE")
        print("=" * 45)
        print(f"  Entradas  : {self.entradas.tolist()}")
        print(f"  Pesos     : {self.pesos.tolist()}")
        print(f"  Sesgo     : {self.sesgo}")
        print("-" * 45)
        print(f"  Suma ponderada  (z) : {self.z:.6f}")
        print(f"  Sigmoide σ(z)       : {self.salida:.6f}")
        print(f"  Derivada σ'(z)      : {self.sigmoide_derivada(self.z):.6f}")
        print("=" * 45)
        
# ─────────────────────────────────────────
#  2. DATOS DEL PROBLEMA
# ─────────────────────────────────────────

entradas = [3,  4,  -2]
pesos    = [0.2, 0.6, 0.01]
sesgo    = 0

# ─────────────────────────────────────────
#  3. EJECUCIÓN
# ─────────────────────────────────────────

perceptron = Perceptron(entradas, pesos, sesgo)
perceptron.forward()
perceptron.mostrar_resultado()


# ─────────────────────────────────────────
#  4. VISUALIZACIÓN DE LA CURVA SIGMOIDE
# ─────────────────────────────────────────

z_vals = np.linspace(-10, 10, 300)
s_vals = Perceptron.sigmoide(z_vals)

plt.figure(figsize=(8, 4))
plt.plot(z_vals, s_vals, color='royalblue', linewidth=2.5, label='σ(z)')

# Marcar el punto calculado
z_punto = perceptron.z
s_punto = perceptron.salida
plt.scatter(z_punto, s_punto, color='red', s=100, zorder=5,
            label=f'Nuestro perceptrón\nz={z_punto:.3f}, σ={s_punto:.4f}')
plt.axvline(z_punto, color='red', linestyle='--', alpha=0.4)
plt.axhline(s_punto, color='red', linestyle='--', alpha=0.4)

plt.title('Función Sigmoide — Perceptrón Simple', fontsize=13)
plt.xlabel('z  (suma ponderada)')
plt.ylabel('σ(z)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('sigmoide_plot.png', dpi=150)
plt.show()
print("Gráfica guardada como 'sigmoide_plot.png'")