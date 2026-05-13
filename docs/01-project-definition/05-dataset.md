# dataset

## what is ravdess?

the ryerson audio-visual database of emotional speech and song ([ravdess](https://affectivedatascience.com/datasets.html#ravdess)) is a collection of 24 professional actors (12 male, 12 female) acting out emotions through speech and song. each clip was recorded in a studio, validated by 247 human raters, and labelled with the intended emotion. think of it as "actors performing emotions on demand." total size: 24.8 gb across 7356 files.

the ravdess was developed by dr steven r. livingstone, who now leads the [affective data science lab](https://affectivedatascience.com), and dr frank a. russo who leads the [smart lab](https://psychlabs.torontomu.ca/smartlab/).

## construction and validation

full details in the [plos one paper](https://doi.org/10.1371/journal.pone.0196391). each file was rated 10 times on emotional validity, intensity, and genuineness by 247 untrained north american adult raters. high levels of emotional validity, interrater reliability, and test-retest reliability are reported. a further 72 participants provided test-retest data. validation data is open-access with the paper.

## the full dataset (7356 files)

3 formats for every recording:

| format | extension | specs |
|--------|-----------|-------|
| audio-only | .wav | 16-bit, 48khz, mono |
| audio-video | .mp4 | 720p h.264, aac 48khz |
| video-only | .mp4 | no sound |

each format has 2 vocal channels:

| channel | what they say | audio-only files |
|---------|---------------|-----------------|
| speech | two lexically-matched statements in neutral north american accent | 1440 |
| song | same emotions but sung (actor 18 has no song files) | 1012 |
| **total audio-only** | | **2452** |

### file counts by category

| category | files | calculation |
|----------|-------|-------------|
| audio speech | 1440 | 60 trials x 24 actors |
| audio song | 1012 | 44 trials x 23 actors |
| av + video speech | 2880 | 60 trials x 2 modalities x 24 actors |
| av + video song | 2024 | 44 trials x 2 modalities x 23 actors |
| **grand total** | **7356** | |

**our project uses audio-only speech + audio-only song only (2452 files). video files are irrelevant.**

## the actors (who)

24 actors, each with id 01-24. odd = male, even = female.

| gender | count | actor ids |
|--------|-------|-----------|
| male | 12 | 01, 03, 05, 07, 09, 11, 13, 15, 17, 19, 21, 23 |
| female | 12 | 02, 04, 06, 08, 10, 12, 14, 16, 18, 20, 22, 24 |

every actor performs every emotion at every intensity with every statement and repetition. speech: 60 files per actor. song: 44 files per actor (no actor 18 in song).

## the emotions

### speech: 8 emotions

| code | emotion | normal intensity (01) | strong intensity (02) | total files |
|------|---------|----------------------|----------------------|-------------|
| 01 | neutral | yes | no | 96 |
| 02 | calm | yes | yes | 192 |
| 03 | happy | yes | yes | 192 |
| 04 | sad | yes | yes | 192 |
| 05 | angry | yes | yes | 192 |
| 06 | fearful | yes | yes | 192 |
| 07 | disgust | yes | yes | 192 |
| 08 | surprised | yes | yes | 192 |

### song: 6 emotions

same as speech minus disgust(07) and surprised(08). 92 files for neutral, 184 each for calm-sad.

### what emotions sound like

| emotion | acoustic signature |
|---------|-------------------|
| neutral | flat, monotone, like reading a shopping list |
| calm | relaxed, soft, steady breath rhythm |
| happy | bright, rising pitch, faster pace |
| sad | slow, low pitch, quiet, pauses |
| angry | loud, harsh, fast, wide pitch range |
| fearful | shaky, high pitch, breathy, tense |
| disgust | drawn-out, guttural, contemptuous tone |
| surprised | sudden, high pitch, variable pace |

## file naming convention

each file has a unique 7-part identifier: `MODALITY-CHANNEL-EMOTION-INTENSITY-STATEMENT-REPETITION-ACTOR.ext`

| position | field | values | meaning |
|----------|-------|--------|---------|
| 1 | modality | 01 = full-av, 02 = video-only, **03 = audio-only** | media type |
| 2 | vocal channel | **01 = speech**, 02 = song | how the emotion is expressed |
| 3 | emotion | 01-08 | the target class (see emotion table above) |
| 4 | intensity | 01 = normal, 02 = strong | emotional intensity (neutral has no strong) |
| 5 | statement | 01 = "kids are talking by the door", 02 = "dogs are sitting by the door" | lexical content |
| 6 | repetition | 01 = 1st, 02 = 2nd | take number |
| 7 | actor | 01-24 | speaker id (odd=male, even=female) |

### examples

`03-01-05-02-01-01-11.wav` -> audio-only, speech, **angry**, strong, statement 1, 1st rep, **actor 11 (male)**.

`03-02-04-01-02-02-08.wav` -> audio-only, song, **sad**, normal, statement 2, 2nd rep, **actor 08 (female)**.

`02-01-06-01-02-01-12.mp4` -> video-only, speech, **fearful**, normal, statement 2, 1st rep, **actor 12 (female)**.

## the variables (what we can control)

| variable | values | relevance |
|----------|--------|-----------|
| emotion | 6-8 labels | the target class |
| intensity | normal / strong | harder classification? strong = more exaggerated cues |
| statement | 2 sentences | should not matter (same content, different words) |
| actor | 24 people | cross-speaker generalization (the hard problem) |
| gender | male / female | can the model work across genders? |

## our data split (by actor, not by file)

speaker-disjoint split to test generalization to unseen speakers.

| split | actors | speech files | song files | total |
|-------|--------|-------------|------------|-------|
| **train** | 01-19 (18 for song) | 1140 | 792 | 1932 |
| **val** | 20, 21, 22 | 180 | 132 | 312 |
| **test** | 23, 24 | 120 | 88 | 208 |

location on disk:

```
data/
  train/speech/Actor_01..19/
  train/song/Actor_01..17,19/
  val/speech/Actor_20,21,22/
  val/song/Actor_20,21,22/
  test/speech/Actor_23,24/
  test/song/Actor_23,24/
```

## common confusions to expect

the model will likely confuse emotions that share the same energy level:

| energy level | emotions | acoustic signature |
|-------------|----------|-------------------|
| **high energy** | angry, fearful, surprised, happy | loud, fast, wide pitch range |
| **low energy** | sad, calm, neutral | quiet, slow, narrow pitch range |

common confusable pairs: angry<->fearful, sad<->calm, surprised<->happy. even humans confuse these.

## watch examples

- [ravdess speech sample](https://www.youtube.com/watch?v=Y7OQoNEu3dY)
- [ravdess song sample](https://www.youtube.com/watch?v=XQkmH4oYZkg)

## citing ravdess

academic papers:
> livingstone sr, russo fa (2018) the ryerson audio-visual database of emotional speech and song (ravdess): a dynamic, multimodal set of facial and vocal expressions in north american english. plos one 13(5): e0196391. https://doi.org/10.1371/journal.pone.0196391.

personal use: link to zenodo page - https://zenodo.org/record/1188976

## data links

- ravdess on zenodo: https://zenodo.org/record/1188976
- orvile/ravdess-dataset on [kaggle](https://www.kaggle.com/datasets/orvile/ravdess-dataset)
- uwrfkaggler/ravdess-emotional-speech-audio on [kaggle](https://www.kaggle.com/datasets/uwrfkaggler/ravdess-emotional-speech-audio)
- facial landmark tracking dataset: [zenodo](https://zenodo.org/records/3255102)
- constructing and validating ser with ravdess: [plos one](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0196391)
