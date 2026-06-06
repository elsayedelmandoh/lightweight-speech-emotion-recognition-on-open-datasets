"""1d cnn model for log-mel-spectrogram speech emotion recognition.

architecture (per neumann & vu, interspeech 2017, simplified for cpu):
    input:  (batch, n_mels, time_frames)  e.g. (B, 128, 251)
    conv1d( n_mels -> 64,  k=5, pad=2 ) -> bn -> relu -> maxpool(2)
    conv1d( 64   -> 128, k=5, pad=2 ) -> bn -> relu -> maxpool(2)
    conv1d( 128  -> 128, k=3, pad=1 ) -> bn -> relu -> adaptiveavgpool(1)
    dropout -> linear(128, num_classes)

~150k parameters, <600 kb on disk. designed for cpu inference.

public api:
    LightweightCNN1D           - the architecture
    MelSpectrogramDataset      - dataset with optional specaugment
    train_cnn                  - full training loop (adamw + onecyclelr + label smoothing + early stopping)
    save_cnn                   - save state dict to disk
    load_cnn                   - load state dict from disk into a fresh model
    predict_cnn                - inference: returns (preds, probs)
    count_parameters           - trainable parameter count
    cpu_inference_latency      - per-sample cpu latency benchmark
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset

from src.config.config import settings


class MelSpectrogramDataset(Dataset):
    """torch dataset for log-mel-spectrograms with optional specaugment.

    args:
        X: array of shape (n_samples, n_mels, time_frames), already
            per-sample normalized in extract_logmel.
        y: int labels of shape (n_samples,).
        augment: if true, apply specaugment (time + frequency masking)
            at training time.
    """

    def __init__(self, X, y, augment: bool = False):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.long)
        self.augment = augment

    def __len__(self) -> int:
        return len(self.y)

    def spec_augment(
        self, x: torch.Tensor,
        n_time_mask: int = 2, n_freq_mask: int = 2,
        time_mask_max: int = 30, freq_mask_max: int = 12,
    ) -> torch.Tensor:
        """apply specaugment: time warping skipped (slow), only masks."""
        n_mels, n_frames = x.shape
        for _ in range(n_time_mask):
            t = torch.randint(0, time_mask_max + 1, (1,)).item()
            t0 = torch.randint(0, max(1, n_frames - t), (1,)).item()
            x[:, t0:t0 + t] = 0
        for _ in range(n_freq_mask):
            f = torch.randint(0, freq_mask_max + 1, (1,)).item()
            f0 = torch.randint(0, max(1, n_mels - f), (1,)).item()
            x[f0:f0 + f, :] = 0
        return x

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        x = self.X[idx].clone()
        y = self.y[idx]
        if self.augment:
            x = self.spec_augment(
                x,
                n_time_mask=settings.SPEC_AUGMENT_N_TIME,
                n_freq_mask=settings.SPEC_AUGMENT_N_FREQ,
                time_mask_max=settings.SPEC_AUGMENT_TIME_MASK,
                freq_mask_max=settings.SPEC_AUGMENT_FREQ_MASK,
            )
        return x, y


class LightweightCNN1D(nn.Module):
    """lightweight 1d cnn for log-mel-spectrogram emotion classification.

    total params: ~150k (small enough for fast cpu inference).
    receptive field covers ~17 time frames at the third conv layer.

    args:
        n_mels: number of mel bands (default: settings.N_MELS = 128).
        num_classes: number of output classes (default: settings.NUM_CLASSES).
        dropout: dropout rate (default: settings.CNN_DROPOUT = 0.3).
    """

    def __init__(
        self,
        n_mels: Optional[int] = None,
        num_classes: Optional[int] = None,
        dropout: Optional[float] = None,
    ):
        super().__init__()
        if n_mels is None:
            n_mels = settings.N_MELS
        if num_classes is None:
            num_classes = settings.NUM_CLASSES
        if dropout is None:
            dropout = settings.CNN_DROPOUT

        self.conv1 = nn.Sequential(
            nn.Conv1d(n_mels, 64, kernel_size=5, padding=2),
            nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=2),
        )
        self.conv2 = nn.Sequential(
            nn.Conv1d(64, 128, kernel_size=5, padding=2),
            nn.BatchNorm1d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=2),
        )
        self.conv3 = nn.Sequential(
            nn.Conv1d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool1d(1),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(dropout),
            nn.Linear(128, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, n_mels, time_frames)
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        return self.classifier(x)


def count_parameters(model: nn.Module) -> int:
    """return total trainable parameters in a model."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def cpu_inference_latency(
    model: nn.Module,
    n_mels: Optional[int] = None,
    time_frames: int = 251,
    n_runs: int = 200,
    device: str = 'cpu',
) -> dict:
    """measure per-sample cpu inference latency in milliseconds.

    args:
        model: a torch nn.Module already moved to the target device.
        n_mels: number of mel bands (default: settings.N_MELS).
        time_frames: time frames per sample.
        n_runs: number of timed forward passes (per-sample, batch=1).
        device: 'cpu' or 'cuda'.

    returns:
        dict with mean_ms, std_ms, p50_ms, p99_ms.
    """
    if n_mels is None:
        n_mels = settings.N_MELS
    model = model.to(device)
    model.eval()
    sample = torch.randn(1, n_mels, time_frames, device=device)

    # warmup
    with torch.no_grad():
        for _ in range(20):
            _ = model(sample)

    timings = []
    with torch.no_grad():
        for _ in range(n_runs):
            t0 = time.perf_counter()
            _ = model(sample)
            t1 = time.perf_counter()
            timings.append((t1 - t0) * 1000.0)

    timings = np.asarray(timings)
    return {
        'mean_ms': float(timings.mean()),
        'std_ms':  float(timings.std()),
        'p50_ms':  float(np.percentile(timings, 50)),
        'p99_ms':  float(np.percentile(timings, 99)),
        'device':  device,
        'n_runs':  n_runs,
    }


def train_cnn(
    X_train: np.ndarray, y_train: np.ndarray,
    X_val: np.ndarray,   y_val: np.ndarray,
    device: Optional[str] = None,
    save_path: Optional[Path] = None,
) -> Tuple[LightweightCNN1D, dict]:
    """full training loop for the 1d cnn.

    uses settings for all hyperparameters:
        settings.CNN_1D_EPOCHS, settings.CNN_1D_BATCH_SIZE,
        settings.CNN_1D_PATIENCE, settings.LEARNING_RATE,
        settings.WEIGHT_DECAY, settings.LABEL_SMOOTHING,
        settings.SPEC_AUGMENT_*, settings.N_MELS, settings.NUM_CLASSES,
        settings.CNN_DROPOUT, settings.SEED.

    optimizer: adamw
    scheduler: onecyclelr (max_lr = 3 * lr)
    loss: cross-entropy with label smoothing
    augmentation: specaugment in the training dataset
    early stopping: on val acc with patience = settings.CNN_1D_PATIENCE

    args:
        X_train, y_train: training set (n, n_mels, time_frames) and labels
        X_val,   y_val:   validation set
        device:   'cpu' or 'cuda' (default: settings.TORCH_DEVICE)
        save_path: optional path to save the best model state dict

    returns:
        (best_model, history) where history is a dict with
        'train_loss', 'train_acc', 'val_loss', 'val_acc' lists.
    """
    if device is None:
        device = settings.TORCH_DEVICE

    torch.manual_seed(settings.SEED)
    np.random.seed(settings.SEED)

    train_dataset = MelSpectrogramDataset(X_train, y_train, augment=True)
    val_dataset   = MelSpectrogramDataset(X_val,   y_val,   augment=False)
    train_loader = DataLoader(train_dataset, batch_size=settings.CNN_1D_BATCH_SIZE,
                              shuffle=True,  num_workers=0, pin_memory=True)
    val_loader   = DataLoader(val_dataset,   batch_size=settings.CNN_1D_BATCH_SIZE,
                              shuffle=False, num_workers=0, pin_memory=True)

    model = LightweightCNN1D(
        n_mels=settings.N_MELS,
        num_classes=settings.NUM_CLASSES,
        dropout=settings.CNN_DROPOUT,
    ).to(device)

    criterion = nn.CrossEntropyLoss(label_smoothing=settings.LABEL_SMOOTHING)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=settings.LEARNING_RATE,
        weight_decay=settings.WEIGHT_DECAY,
    )
    scheduler = torch.optim.lr_scheduler.OneCycleLR(
        optimizer,
        max_lr=settings.LEARNING_RATE * 3,
        total_steps=settings.CNN_1D_EPOCHS * len(train_loader),
        pct_start=0.1,
        anneal_strategy='cos',
    )

    history = {
        'train_loss': [], 'train_acc': [],
        'val_loss':   [], 'val_acc':   [],
    }
    best_val_acc     = 0.0
    best_val_loss    = float('inf')
    patience_counter = 0

    for epoch in range(settings.CNN_1D_EPOCHS):
        model.train()
        train_loss, train_correct = 0.0, 0
        for X_batch, y_batch in train_loader:
            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device)

            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()
            scheduler.step()

            train_loss += loss.item() * X_batch.size(0)
            train_correct += (outputs.argmax(1) == y_batch).sum().item()

        train_loss /= len(train_dataset)
        train_acc   = train_correct / len(train_dataset)

        model.eval()
        val_loss, val_correct = 0.0, 0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                X_batch = X_batch.to(device)
                y_batch = y_batch.to(device)
                outputs = model(X_batch)
                loss    = criterion(outputs, y_batch)
                val_loss   += loss.item() * X_batch.size(0)
                val_correct += (outputs.argmax(1) == y_batch).sum().item()
        val_loss /= len(val_dataset)
        val_acc   = val_correct / len(val_dataset)

        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)

        print(f"Epoch [{epoch+1:02d}/{settings.CNN_1D_EPOCHS}] "
              f"Train Loss: {train_loss:.4f} Acc: {train_acc*100:.2f}% | "
              f"Val Loss: {val_loss:.4f} Acc: {val_acc*100:.2f}%")

        if val_acc > best_val_acc:
            best_val_acc  = val_acc
            best_val_loss = val_loss
            if save_path is not None:
                torch.save(model.state_dict(), save_path)
            print(f"   Best model saved! Val Acc: {best_val_acc*100:.2f}%")
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= settings.CNN_1D_PATIENCE:
                print(f"\nEarly stopping at epoch {epoch+1}")
                break

    return model, history


def save_cnn(model: LightweightCNN1D, save_path: Path) -> None:
    """save the 1d cnn state dict to disk."""
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), save_path)


def load_cnn(
    save_path: Path,
    n_mels: Optional[int] = None,
    num_classes: Optional[int] = None,
    dropout: Optional[float] = None,
    device: Optional[str] = None,
) -> LightweightCNN1D:
    """load a 1d cnn state dict from disk into a fresh model.

    args:
        save_path: path to a .pth file saved by save_cnn() or train_cnn()
        n_mels, num_classes, dropout: model architecture params
            (default: settings.N_MELS, settings.NUM_CLASSES, settings.CNN_DROPOUT)
        device: 'cpu' or 'cuda' (default: settings.TORCH_DEVICE)

    returns:
        a LightweightCNN1D in eval mode, loaded onto the target device.
    """
    if device is None:
        device = settings.TORCH_DEVICE
    model = LightweightCNN1D(
        n_mels=n_mels, num_classes=num_classes, dropout=dropout,
    )
    model.load_state_dict(torch.load(save_path, map_location=device, weights_only=True))
    model.to(device)
    model.eval()
    return model


def predict_cnn(
    model: LightweightCNN1D,
    X: np.ndarray,
    batch_size: int = 32,
    device: Optional[str] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """run inference on a batch of mel-spectrograms.

    args:
        model: a LightweightCNN1D already in eval mode
        X: np.ndarray of shape (n_samples, n_mels, time_frames)
        batch_size: inference batch size
        device: 'cpu' or 'cuda' (default: settings.TORCH_DEVICE)

    returns:
        (preds, probs) - preds has shape (n_samples,),
        probs has shape (n_samples, num_classes).
    """
    if device is None:
        device = settings.TORCH_DEVICE
    model = model.to(device)
    model.eval()

    dataset = MelSpectrogramDataset(X, np.zeros(len(X)), augment=False)
    loader  = DataLoader(dataset, batch_size=batch_size,
                         shuffle=False, num_workers=0, pin_memory=True)
    all_preds, all_probs = [], []
    with torch.no_grad():
        for X_batch, _ in loader:
            X_batch = X_batch.to(device)
            outputs = model(X_batch)
            probs = F.softmax(outputs, dim=1)
            all_probs.append(probs.cpu().numpy())
            all_preds.append(outputs.argmax(1).cpu().numpy())
    preds = np.concatenate(all_preds)
    probs = np.concatenate(all_probs)
    return preds, probs
