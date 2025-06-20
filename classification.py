# -*- coding: utf-8 -*-
import json
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text, export_graphviz, plot_tree
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import seaborn as sns
import graphviz
import re

# Função para padronizar descrições de miômeros e mioseptos
def padronizar_mioseptos(text):
    if not isinstance(text, str) or text == "não caracterizado":
        return text

    text = text.lower()
    text = re.sub(r'[^\w\s/.\àáâãéêíóôõúüç0-9]', '', text, flags=re.IGNORECASE)

    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Função para carregar dados do JSON
def carregar_dados(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        dados = json.load(file)
    
    # Converter para DataFrame
    df = pd.DataFrame(dados)
    
    # Padronizar colunas
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    
    # Padronizar valores textuais
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip().str.lower()
    
    # Aplicar padronização na coluna miomeros_mioseptos
    if 'miomeros_mioseptos' in df.columns:
        df['miomeros_mioseptos'] = df['miomeros_mioseptos'].apply(padronizar_mioseptos)
    
    return df

# 2. Preparar dados
def preparar_dados(df):
    label_encoders = {}
    # Selecionar apenas as colunas presentes no JSON
    features = ["cor_aspecto", "septo_horizontal", "perimisio", "miomeros_mioseptos", "musculatura"]
    
    # Garantir que apenas colunas existentes sejam usadas
    features = [f for f in features if f in df.columns]
    
    X = df[features].copy()
    y = df["especie"].copy()

    for col in features:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le

    le_y = LabelEncoder()
    y = le_y.fit_transform(y)

    return X.values, y, label_encoders, le_y, features

def calcular_max_depth(num_amostras):
    if num_amostras < 2:
        return 3
    base_depth = num_amostras // 2
    return max(3, min(num_amostras, base_depth))

def treinar_arvore(X, y):
    num_amostras = len(X)
    max_depth = calcular_max_depth(num_amostras)

    print(f"\nNúmero de amostras: {num_amostras} -> max_depth calculado: {max_depth}")

    model = DecisionTreeClassifier(criterion="entropy", max_depth=max_depth, random_state=42)
    model.fit(X, y)
    return model

# 5. Prever nova entrada
def prever(model, label_encoders, le_y, features, entrada):
    entrada_proc = []
    for i, nome in enumerate(features):
        valor = entrada[i].strip().lower()
        if valor in label_encoders[nome].classes_:
            codificado = label_encoders[nome].transform([valor])[0]
            entrada_proc.append(codificado)
        else:
            print(f"Valor inválido para '{nome}': {valor}")
            print("Valores válidos:", label_encoders[nome].classes_)
            return None
    entrada_np = np.array(entrada_proc).reshape(1, -1)
    pred = model.predict(entrada_np)
    especie = le_y.inverse_transform(pred)[0]
    return especie

# 6. Matriz de confusão usando os próprios dados de treinamento
def matriz_confusao_treinamento(modelo, X, y, le_y):
    y_pred = modelo.predict(X)
    cm = confusion_matrix(y, y_pred)
    acc = accuracy_score(y, y_pred)

    print("\nMatriz de Confusão (mesmo conjunto de treino):")
    print(cm)
    print("Classes:", le_y.classes_)
    print(f"Precisão geral: {acc:.4f}")

    return cm, le_y.classes_

# 7. Função para validação cruzada com cálculo automático de profundidade
def validacao_cruzada(X, y, le_y):
    unique, counts = np.unique(y, return_counts=True)
    class_counts = dict(zip(le_y.inverse_transform(unique), counts))
    num_classes = len(unique)

    print("\nContagem de amostras por classe:")
    for cls, count in class_counts.items():
        print(f"Classe '{cls}': {count} amostra(s)")

    min_samples_per_class = np.min(counts)

    if min_samples_per_class < 2:
        print(f"\nAviso: Algumas classes têm menos de 2 amostras (mínimo: {min_samples_per_class}). "
              "Validação cruzada não pode ser realizada.")
        return None

    cv = min(min_samples_per_class, 5)
    print(f"\nUsando cv={cv} para validação cruzada.")
    num_amostras = len(y)
    max_depth = calcular_max_depth(num_amostras)

    model = DecisionTreeClassifier(criterion="entropy", max_depth=max_depth, random_state=42)
    scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')

    # Plotando gráfico de barras
    plt.figure(figsize=(10, 6))
    barras = plt.bar(
        x=[f'Execução {i+1}' for i in range(cv)],
        height=scores,
        color='#4a90e2',
        edgecolor='black'
    )

    for barra in barras:
        height = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            height + 0.01,
            f'{height:.2f}',
            ha='center',
            va='bottom',
            fontsize=10
        )

    plt.title('Desempenho de Classificação por Execução da Validação Cruzada', fontsize=14)
    plt.xlabel('Execuções', fontsize=12)
    plt.ylabel('Precisão', fontsize=12)
    plt.ylim(0, 1.05)
    plt.legend(['Precisão por Execução'], loc='lower right')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

    print(f"\nMédia da precisão: {scores.mean():.4f}")

    return scores

# 8. Plotar matriz de confusão
def plotar_matriz_confusao(cm, classes):
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt="d", cmap="YlOrRd", xticklabels=classes, yticklabels=classes,
                cbar_kws={'label': 'Contagem'})
    plt.xlabel("Classe Predita")
    plt.ylabel("Classe Verdadeira")
    plt.title("Matriz de Confusão")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# Função principal
def main():
    # Carregar dados do JSON
    json_path = "dados_pescados.json"  # Substitua pelo caminho do seu arquivo JSON
    df = carregar_dados(json_path)
    
    # Preparar dados
    X, y, label_encoders, le_y, feature_names = preparar_dados(df)
    
    # Realizar validação cruzada
    scores = validacao_cruzada(X, y, le_y)
    
    # Treinar o modelo final
    modelo = treinar_arvore(X, y)
    
    # Avaliar modelo
    cm, classes = matriz_confusao_treinamento(modelo, X, y, le_y)
    plotar_matriz_confusao(cm, classes)

    # Exemplo de previsão
    entrada = [
        "rosado",          # cor_aspecto
        "visível",         # septo_horizontal
        "ausente",         # perimisio
        "conformação padrão",  # miomeros_mioseptos (padronizado)
        "branca"           # musculatura
    ]
    
    resultado = prever(modelo, label_encoders, le_y, feature_names, entrada)
    
    if resultado:
        print(f"\nResultado da previsão: A espécie prevista é '{resultado.upper()}'")
        print("Características usadas:", entrada)

if __name__ == "__main__":
    main()