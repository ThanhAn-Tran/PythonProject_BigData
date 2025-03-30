import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix


class AirQualityModelTrainer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
        self.model = None
        self.scaler = StandardScaler()

    def preprocess_data(self):
        X = self.df.drop(columns=['AQI_Label'])
        y = self.df['AQI_Label'].astype(int)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)

        return X_train, X_test, y_train, y_test

    def build_model(self, input_shape, num_classes):
        self.model = keras.Sequential([
            keras.layers.Dense(256, activation='relu', input_shape=(input_shape,)),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.Dense(num_classes, activation='softmax')
        ])
        self.model.compile(optimizer='adam',
                           loss='sparse_categorical_crossentropy',
                           metrics=['accuracy'])

    def train_model(self, X_train, y_train, X_test, y_test, epochs=100, batch_size=16):
        early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        history = self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,
                                 validation_data=(X_test, y_test), callbacks=[early_stopping])
        return history

    def evaluate_model(self, X_test, y_test):
        test_loss, test_acc = self.model.evaluate(X_test, y_test)
        print(f"Test accuracy: {test_acc * 100:.2f}%")

        y_pred = np.argmax(self.model.predict(X_test), axis=1)
        print(classification_report(y_test, y_pred))

        return test_loss, test_acc

    def plot_history(self, history):
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(history.history['accuracy'], label='Train Accuracy')
        plt.plot(history.history['val_accuracy'], label='Val Accuracy')
        plt.legend()
        plt.title("Model Accuracy")

        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'], label='Train Loss')
        plt.plot(history.history['val_loss'], label='Val Loss')
        plt.legend()
        plt.title("Model Loss")
        plt.show()

    def save_model(self, model_path):
        self.model.save(model_path)


if __name__ == "__main__":
    trainer = AirQualityModelTrainer("Data/processed_AQI_data.csv")
    X_train, X_test, y_train, y_test = trainer.preprocess_data()
    trainer.build_model(input_shape=X_train.shape[1], num_classes=len(np.unique(y_train)))
    history = trainer.train_model(X_train, y_train, X_test, y_test)
    trainer.evaluate_model(X_test, y_test)
    trainer.plot_history(history)
    trainer.save_model("model_ML/air_quality_model.h5")
