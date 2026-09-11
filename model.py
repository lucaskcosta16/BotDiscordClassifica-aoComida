from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

def get_class(model_path, labels_path, image_path):
    
    # configuração do numpy para não exibir notação científica
    np.set_printoptions(suppress=True)

    # Carregar o modelo treinado
    model = load_model(model_path, compile=False)

    # Carregar os rótulos das classes
    class_names = open(labels_path, "r", encoding="utf-8").readlines()

    # criar um array numpy com o tamanho da imagem de entrada do modelo
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    #preparar a imagem para o modelo
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    #converter a imagem em um array numpy
    image_array = np.asarray(image)

    #normalizar a imagem
    normalized_image_array = (image_array.astype(np.float32) / 127.0)-1

    #carregar a imagem normalizada no array de dados
    data[0] = normalized_image_array

    #fazer a previsão
    prediction = model.predict(data)
    index = np.argmax(prediction)

    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return class_name[2:], confidence_score
