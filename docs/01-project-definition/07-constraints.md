# project constraints and assumptions

## constraints

- **cpu inference only.** no gpu required at inference time. model must run on a single cpu core in < 100ms per clip.
- **model size < 5mb.** must fit comfortably in memory on edge/embedded devices.
- **open datasets only.** ravdess (primary). crema-d (optional secondary). no proprietary data.
- **no real-time streaming.** batch inference on fixed-length clips only. streaming is explicitly out of scope.
- **no data augmentation beyond standard audio transforms.** no generative augmentation (tts, voice conversion).

## assumptions

- input audio is single-channel, 16-bit, 48khz wav (ravdess native format). resampling may be needed for other datasets.
- clips are short (2-5 seconds). no need for chunking or long-form handling.
- emotion labels are discrete (8-class from ravdess). no continuous arousal/valence modeling.
- acted speech (ravdess) is a reasonable proxy for evaluating model architecture, even if it overestimates real-world performance.
- sufficient compute available for training (single gpu preferred, cpu acceptable with longer training time).

## non-goals

- real-time or streaming inference.
- multilingual or cross-lingual ser.
- speech-to-text or content analysis.
- production-grade serving infrastructure.
