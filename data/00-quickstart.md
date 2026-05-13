# ravdess dataset explained

## what is ravdess?

a collection of 24 professional actors (12 male, 12 female) acting out emotions through speech and song. each clip was recorded in a studio, validated by 247 human raters, and labelled with the intended emotion. think of it as "actors performing emotions on demand."

## the full dataset (24.8 gb, 7356 files)

the complete download has 3 formats for every recording:

| format | extension | what it is |
|--------|-----------|------------|
| audio-only | .wav | just sound, 16-bit, 48khz, mono |
| audio-video | .mp4 | face + voice together |
| video-only | .mp4 | just video, no sound |

**we only use audio-only.** video files are irrelevant for this project.

additionally, each format has 2 vocal channels:

| channel | files | what they say |
|---------|-------|---------------|
| speech | 1440 | "kids are talking by the door" / "dogs are sitting by the door" |
| song | 1012 | same emotions but sung (actor 18 has no song files) |

**we use both speech and song** = 1440 + 1012 = 2452 files total.

---

## the actors (who)

24 actors, each with an id from 01 to 24.

| actor id range | count | gender rule |
|---------------|-------|-------------|
| 01 - 24 (odd) | 12 | male |
| 01 - 24 (even) | 12 | female |

every actor performs every emotion at every intensity with every statement and every repetition. 60 speech files per actor. 44 song files per actor.

---

## the emotions (what)

### speech has 8 emotions

| code | emotion | intensity 01 (normal) | intensity 02 (strong) |
|------|---------|----------------------|----------------------|
| 01 | neutral | yes | no (only 1 level) |
| 02 | calm | yes | yes |
| 03 | happy | yes | yes |
| 04 | sad | yes | yes |
| 05 | angry | yes | yes |
| 06 | fearful | yes | yes |
| 07 | disgust | yes | yes |
| 08 | surprised | yes | yes |

96 files for neutral. 192 files for every other emotion (96 normal + 96 strong).

### song has 6 emotions

same as speech but without disgust(07) and surprised(08). 92 files for neutral, 184 for every other emotion.

### what the emotions sound like

- **neutral**: flat, monotone, no emotional colour. like reading a shopping list.
- **calm**: relaxed, soft, steady breathing rhythm.
- **happy**: bright, rising pitch, faster pace.
- **sad**: slow, low pitch, quiet, pauses.
- **angry**: loud, harsh, fast, wide pitch range.
- **fearful**: shaky, high pitch, breathy, tense.
- **disgust**: drawn-out, guttural, contemptuous tone.
- **surprised**: sudden, high pitch, variable pace.

---

## the filename (how to read it)

each file is named `03-CHANNEL-EMOTION-INTENSITY-STATEMENT-REPETITION-ACTOR.wav`

### example: `03-01-05-02-01-01-11.wav`

| part | value | means |
|------|-------|-------|
| 03 | audio-only | just sound (not video) |
| 01 | speech | speaking (not singing) |
| 05 | angry | emotion = angry |
| 02 | strong | intense version |
| 01 | statement 1 | "kids are talking by the door" |
| 01 | repetition 1 | first take |
| 11 | actor 11 | male (odd number) |

so this is: **actor 11 (male) saying "kids are talking by the door" in a strong angry voice.**

### example: `03-02-04-01-02-02-08.wav`

| part | value | means |
|------|-------|-------|
| 03 | audio-only | just sound |
| 02 | song | singing |
| 04 | sad | emotion = sad |
| 01 | normal | not intense |
| 02 | statement 2 | "dogs are sitting by the door" |
| 02 | repetition 2 | second take |
| 08 | actor 08 | female (even number) |

so this is: **actor 08 (female) singing "dogs are sitting by the door" in a normal sad voice.**

---

## the variables (what we can control)

| variable | values | what it affects |
|----------|--------|----------------|
| emotion | 6-8 labels | the target class |
| intensity | normal / strong | harder to classify? strong = more exaggerated |
| statement | 2 sentences | should not matter (same content) |
| actor | 24 people | the hard problem: does it work on new speakers? |
| gender | male / female | can the model work across genders? |

---

## our data split (by actor, not by file)

we split by actor to test whether the model works on **unseen speakers**.

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

---

## what we are trying to do

1. train a computer to look at a sound clip and guess the emotion.
2. the computer never knows which actor is speaking (we held out actors 23, 24 for final testing).
3. we compare two approaches:
   - **old way**: extract mfcc numbers, feed to svm
   - **new way**: convert sound to mel spectrogram picture, feed to 1d cnn
4. measure: accuracy, which emotions get confused, does it work on new speakers, how fast is it on cpu.

---

## common confusions to expect

the model will likely confuse emotions that share the same **energy level**:

- **high energy**: angry, fearful, surprised, happy (loud, fast, wide pitch range)
- **low energy**: sad, calm, neutral (quiet, slow, narrow pitch range)
- **confusable pairs**: angry<->fearful, sad<->calm, surprised<->happy

this is normal. even humans confuse these.
