import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Force non-interactive backend for matplotlib to avoid GUI/Qt errors
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

def main():
    # Model path
    model_path = "laptop_classifier.keras"
    if not os.path.exists(model_path):
        print(f"[ERROR] Model '{model_path}' tidak ditemukan. Silakan jalankan 'train.py' terlebih dahulu.")
        sys.exit(1)
        
    # Default test dataset path
    default_test_path = "test_dataset"
    
    # Check if a custom path is provided as CLI argument
    if len(sys.argv) > 1:
        test_path = sys.argv[1]
    else:
        test_path = default_test_path
        
    print(f"\nEvaluating using test dataset directory: '{test_path}'")
    
    if not os.path.exists(test_path):
        print(f"[ERROR] Folder '{test_path}' tidak ditemukan.")
        print("\nSilakan buat folder tersebut dengan struktur subfolder seperti berikut:")
        print(f"  {test_path}/")
        print("    ├── laptop/      <-- berisi gambar laptop untuk pengujian")
        print("    └── not_laptop/  <-- berisi gambar non-laptop untuk pengujian")
        print(f"\nAtau jalankan: python evaluate.py <path_folder_test_anda>")
        sys.exit(1)
        
    # Load model
    print(f"\n[1/3] Memuat model '{model_path}'...")
    model = load_model(model_path)
    
    # Load dataset test
    print(f"[2/3] Memuat dataset dari '{test_path}'...")
    try:
        test_ds = tf.keras.utils.image_dataset_from_directory(
            test_path,
            image_size=(128, 128),
            batch_size=32,
            shuffle=False # Keep ordered for prediction comparison
        )
    except Exception as e:
        print(f"[ERROR] Gagal memuat dataset: {e}")
        sys.exit(1)
        
    class_names = test_ds.class_names
    print(f"Ditemukan kelas: {class_names}")
    
    # Evaluate model
    print(f"\n[3/3] Melakukan evaluasi model...")
    loss, accuracy = model.evaluate(test_ds, verbose=1)
    
    # Extract labels and predictions
    y_true = []
    y_pred = []
    
    for images, labels in test_ds:
        predictions = model.predict(images, verbose=0)
        y_pred.extend(np.argmax(predictions, axis=1))
        y_true.extend(labels.numpy())
        
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # Output metrics
    print("\n" + "="*50)
    print("HASIL EVALUASI TEST SET")
    print("="*50)
    print(f"Akurasi Test: {accuracy * 100:.2f}%")
    print(f"Loss Test: {loss:.4f}")
    print("="*50)
    
    print("\nCLASSIFICATION REPORT (TEST SET)")
    print("="*50)
    print(classification_report(y_true, y_pred, target_names=class_names))
    
    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    print("="*50)
    print("CONFUSION MATRIX (Console)")
    print("="*50)
    print(f"Classes: {class_names}")
    print(cm)
    print("="*50)
    
    # Plot Confusion Matrix
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges', 
                xticklabels=class_names, yticklabels=class_names,
                cbar=True, annot_kws={"size": 14})
    plt.title('Test Set Confusion Matrix', fontsize=14, pad=15)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.ylabel('True Label', fontsize=12)
    plt.tight_layout()
    
    output_filename = "test_confusion_matrix.png"
    plt.savefig(output_filename)
    print(f"\n[INFO] Plot confusion matrix test disimpan ke '{output_filename}'\n")

if __name__ == "__main__":
    main()
