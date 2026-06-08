import tensorflow as tf
from tensorflow.keras import layers, models, regularizers

# Load Dataset
train_ds = tf.keras.utils.image_dataset_from_directory(
    "dataset",
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(128, 128),
    batch_size=32
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    "dataset",
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(128, 128),
    batch_size=32
)

print("Class Names:", train_ds.class_names)

# Load pretrained MobileNetV2 base model (without ImageNet classification head)
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(128, 128, 3),
    include_top=False,
    weights='imagenet'
)

# Freeze base model layers so we only train the new classifier head (Transfer Learning)
base_model.trainable = False

# Construct custom model
model = models.Sequential([
    # Data Augmentation (Manual, only active during training)
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
    layers.RandomBrightness(0.1),
    
    # Internal rescaling to map raw [0, 255] input to MobileNetV2's required [-1, 1] range
    layers.Rescaling(1./127.5, offset=-1.0),
    
    # Pre-trained base
    base_model,
    
    # Classification head
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(1e-4)),
    layers.Dropout(0.5),
    layers.Dense(2, activation='softmax')
])

# Compile
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Callback for dynamic learning rate decay
lr_callback = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=2,
    min_lr=1e-6,
    verbose=1
)

# Training (Transfer learning converges very quickly, 15 epochs is plenty)
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=15,
    callbacks=[lr_callback]
)

# Save Model
model.save("laptop_classifier.keras")
print("\nModel berhasil disimpan ke 'laptop_classifier.keras'")

# ------------------
# ANALYTICS & RESULTS
# ------------------
import os
import numpy as np
import matplotlib
matplotlib.use('Agg') # Force non-interactive backend to avoid Qt/GUI errors
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

# 1. Plot Training History (Accuracy & Loss)
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs_range = range(len(acc))

plt.figure(figsize=(12, 5))

# Plot Accuracy
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy', color='#0071E3', linewidth=2)
plt.plot(epochs_range, val_acc, label='Validation Accuracy', color='#FF9500', linewidth=2)
plt.legend(loc='lower right')
plt.title('Training & Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.grid(True, linestyle='--', alpha=0.5)

# Plot Loss
plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss', color='#FF3B30', linewidth=2)
plt.plot(epochs_range, val_loss, label='Validation Loss', color='#4CD964', linewidth=2)
plt.legend(loc='upper right')
plt.title('Training & Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig("training_metrics.png")
print("\n[INFO] Plot akurasi & loss disimpan ke 'training_metrics.png'")

# 2. Confusion Matrix & Classification Report
print("\nMenghitung metrik evaluasi pada dataset validasi...")
y_true = []
y_pred = []

for images, labels in val_ds:
    predictions = model.predict(images, verbose=0)
    y_pred.extend(np.argmax(predictions, axis=1))
    y_true.extend(labels.numpy())

y_true = np.array(y_true)
y_pred = np.array(y_pred)
class_names = train_ds.class_names

# Print Text Classification Report
print("\n" + "="*50)
print("CLASSIFICATION REPORT")
print("="*50)
print(classification_report(y_true, y_pred, target_names=class_names))

# Print Text Confusion Matrix
cm = confusion_matrix(y_true, y_pred)
print("="*50)
print("CONFUSION MATRIX (Console)")
print("="*50)
print(f"Classes: {class_names}")
print(cm)
print("="*50)

# Plot Confusion Matrix
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=class_names, yticklabels=class_names,
            cbar=True, annot_kws={"size": 14})
plt.title('Confusion Matrix', fontsize=14, pad=15)
plt.xlabel('Predicted Label', fontsize=12)
plt.ylabel('True Label', fontsize=12)
plt.tight_layout()
plt.savefig("confusion_matrix.png")
print("[INFO] Plot confusion matrix disimpan ke 'confusion_matrix.png'")