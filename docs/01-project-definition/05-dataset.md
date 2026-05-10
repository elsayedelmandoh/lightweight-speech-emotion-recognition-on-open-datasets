# dataset

## The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS)

## Description

The Ryerson Audio-Visual Database of Emotional Speech and Song ([RAVDESS](https://affectivedatascience.com/datasets.html#ravdess)) contains 7356 files (total size: 24.8 GB). The dataset contains 24 professional actors (12 female, 12 male), vocalizing two lexically-matched statements in a neutral North American accent. Speech includes calm, happy, sad, angry, fearful, surprise, and disgust expressions, and song contains calm, happy, sad, angry, and fearful emotions. Each expression is produced at two levels of emotional intensity (normal, strong), with an additional neutral expression. All conditions are available in three modality formats: Audio-only (16bit, 48kHz .wav), Audio-Video (720p H.264, AAC 48kHz, .mp4), and Video-only (no sound).  Note, there are no song files for Actor_18.

The RAVDESS was developed by Dr Steven R. Livingstone, who now leads the Affective Data Science Lab, and Dr Frank A. Russo who leads the SMART Lab.

## Citing the RAVDESS

The RAVDESS is released under a Creative Commons Attribution license, so please cite the RAVDESS if it is used in your work in any form.  Published academic papers should use the academic paper citation for our PLoS1 paper.  Personal works, such as machine learning projects/blog posts, should provide a URL to this Zenodo page, though a reference to our PLoS1 paper would also be appreciated.

## Academic paper citation

> Livingstone SR, Russo FA (2018) The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS): A dynamic, multimodal set of facial and vocal expressions in North American English. PLoS ONE 13(5): e0196391. https://doi.org/10.1371/journal.pone.0196391.

## Personal use citation

Include a link to this Zenodo page - https://zenodo.org/record/1188976

## Example Videos

Watch a sample of the RAVDESS [speech](https://www.youtube.com/watch?v=Y7OQoNEu3dY) and [song](https://www.youtube.com/watch?v=XQkmH4oYZkg) videos.

## Emotion Classification Users

If you're interested in using machine learning to classify emotional expressions with the RAVDESS, please see our new RAVDESS Facial Landmark Tracking data set [Zenodo project page](https://zenodo.org/records/3255102).


## Construction and Validation

Full details on the construction and perceptual validation of the RAVDESS are described in our PLoS ONE paper - https://doi.org/10.1371/journal.pone.0196391.

The RAVDESS contains 7356 files. Each file was rated 10 times on emotional validity, intensity, and genuineness. Ratings were provided by 247 individuals who were characteristic of untrained adult research participants from North America. A further set of 72 participants provided test-retest data. High levels of emotional validity, interrater reliability, and test-retest intrarater reliability were reported. Validation data is open-access, and can be downloaded along with our paper from [PLoS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0196391).

## Contents

### Audio-only files

Audio-only files of all actors (01-24) are available as two separate zip files (~200 MB each):

- Speech file (Audio_Speech_Actors_01-24.zip, 215 MB) contains 1440 files: 60 trials per actor x 24 actors = 1440. 
- Song file (Audio_Song_Actors_01-24.zip, 198 MB) contains 1012 files: 44 trials per actor x 23 actors = 1012.

### Audio-Visual and Video-only files

Video files are provided as separate zip downloads for each actor (01-24, ~500 MB each), and are split into separate speech and song downloads:

- Speech files (Video_Speech_Actor_01.zip to Video_Speech_Actor_24.zip) collectively contains 2880 files: 60 trials per actor x 2 modalities (AV, VO) x 24 actors = 2880.

- Song files (Video_Song_Actor_01.zip to Video_Song_Actor_24.zip) collectively contains 2024 files: 44 trials per actor x 2 modalities (AV, VO) x 23 actors = 2024.

### File Summary

In total, the RAVDESS collection includes 7356 files (2880+2024+1440+1012 files).


## File naming convention

Each of the 7356 RAVDESS files has a unique filename. The filename consists of a 7-part numerical identifier (e.g., 02-01-06-01-02-01-12.mp4). These identifiers define the stimulus characteristics: 

## Filename identifiers 

- Modality (01 = full-AV, 02 = video-only, 03 = audio-only).
- Vocal channel (01 = speech, 02 = song).
- Emotion (01 = neutral, 02 = calm, 03 = happy, 04 = sad, 05 = angry, 06 = fearful, 07 = disgust, 08 = surprised).
- Emotional intensity (01 = normal, 02 = strong). NOTE: There is no strong intensity for the 'neutral' emotion.
- Statement (01 = "Kids are talking by the door", 02 = "Dogs are sitting by the door").
- Repetition (01 = 1st repetition, 02 = 2nd repetition).
- Actor (01 to 24. Odd numbered actors are male, even numbered actors are female).

## Filename example: 02-01-06-01-02-01-12.mp4 

1. Video-only (02)
2. Speech (01)
3. Fearful (06)
4. Normal intensity (01)
5. Statement "dogs" (02)
6. 1st Repetition (01)
7. 12th Actor (12)
8. Female, as the actor ID number is even.


## Data Link: 

- RAVDESS: https://zenodo.org/record/1188976 
- orvile/ravdess-dataset - [kaggle](https://www.kaggle.com/datasets/orvile/ravdess-dataset)
- uwrfkaggler/ravdess-emotional-speech-audio [kaggle](https://www.kaggle.com/datasets/uwrfkaggler/ravdess-emotional-speech-audio)
