import matplotlib.pyplot as plt
import numpy as np

# Exemple de données
data = np.random.random(1024)  # Remplacer par vos données réelles

# Temps associé à chaque point (1 point = 10 microsecondes)
time = np.arange(0, len(data) * 10, 10)  # de 0 à 10230 microsecondes

# Vérifiez la longueur des données et du temps
assert len(time) == len(data), "Les longueurs de 'time' et 'data' doivent être identiques"

# Tracer le graphique
plt.figure(figsize=(10, 6))
plt.plot(time, data)
plt.xlabel('Temps (microsecondes)')
plt.ylabel('Amplitude')
plt.title('Graphique des données avec échelle de temps')
plt.grid(True)
plt.show()
