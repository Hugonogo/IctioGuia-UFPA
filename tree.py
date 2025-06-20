import json
import numpy as np
from collections import Counter
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score, LeaveOneOut, StratifiedKFold
from sklearn.metrics import confusion_matrix

def carregar_dados(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        dados = json.load(file)
    return dados

def preparar_dados(dados):
    label_encoders = {}
    X = []
    y = []
    
    for item in dados:
        features = [
            item["cor_aspecto"],
            item["septo_horizontal"],
            item["perimisio"],
            item["miomeros_mioseptos"],
            item["musculatura"]
        ]
        X.append(features)
        y.append(item["especie"])

    X = np.array(X).T
    for i in range(X.shape[0]):
        le = LabelEncoder()
        X[i] = le.fit_transform(X[i])
        label_encoders[i] = le

    X = X.T.astype(np.float32)

    le_especie = LabelEncoder()
    y = le_especie.fit_transform(y)

    return X, y, label_encoders, le_especie

def treinar_arvore(X, y, max_depth=None):
    modelo = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    modelo.fit(X, y)
    return modelo

def avaliar_modelo(modelo, X, y):
    # Verifica a quantidade mínima de amostras por classe
    min_por_classe = min(Counter(y).values())
    n_splits = min(3, min_por_classe)  # Ajuste automático
    if n_splits < 2:
        print("Não há amostras suficientes para realizar validação cruzada.")
        return

    cv = StratifiedKFold(n_splits=n_splits)
    scores = cross_val_score(modelo, X, y, cv=cv, scoring='accuracy')
    print(f"Acurácia média (validação cruzada com {n_splits} splits): {scores.mean():.4f}")
    print(f"Desvio padrão: {scores.std():.4f}")

def matriz_confusao(modelo, X, y, le_especie):
    loo = LeaveOneOut()
    y_true, y_pred = [], []
    
    for train_idx, test_idx in loo.split(X):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        modelo.fit(X_train, y_train)
        y_pred.append(modelo.predict(X_test)[0])
        y_true.append(y_test[0])
    
    cm = confusion_matrix(y_true, y_pred)
    print("Matriz de confusão:")
    print(cm)
    print("Classes:", le_especie.classes_)

def prever_especie(modelo, label_encoders, le_especie, caracteristicas):
    entrada_numerica = []
    
    for i, valor in enumerate(caracteristicas):
        if valor in label_encoders[i].classes_:
            entrada_numerica.append(label_encoders[i].transform([valor])[0])
        else:
            print(f"Erro: O valor '{valor}' para a característica {i+1} não foi encontrado nos dados de treino.")
            print(f"Valores válidos: {label_encoders[i].classes_.tolist()}")
            return None
    
    entrada_numerica = np.array(entrada_numerica).reshape(1, -1).astype(np.float32)
    
    predicao = modelo.predict(entrada_numerica)
    especie_predita = le_especie.inverse_transform(predicao)
    return especie_predita[0]

dados = carregar_dados('Dados.json')
X, y, label_encoders, le_especie = preparar_dados(dados)

modelo = treinar_arvore(X, y, max_depth=5)
avaliar_modelo(modelo, X, y)
matriz_confusao(modelo, X, y, le_especie)

# Prever nova espécie
caracteristicas = ["rosado", "visível", "ausente", "./Assets/mm16.png", "branca"]
especie = prever_especie(modelo, label_encoders, le_especie, caracteristicas)
print("Espécie predita:", especie)
