## 8. team contributions

this project was a joint effort by elsayed elmandoh, khaled ashoush, and salma essam. we contributed to the full pipeline, code reviews, and the final report.

| notebook | elsayed | khaled | salma |
|----------|---------|--------|-------|
| 00-preliminary-experiments | primary | primary | primary |
| 01 data acquisition | -- | primary | -- |
| 02 eda | -- | primary | primary |
| 03 preprocessing | -- | primary | primary |
| 04 feature engineering | -- | primary | primary |
| 05.1 svm baseline | primary | -- | primary |
| 05.2 cnn 1d | primary | -- | -- |
| 06.1 svm evaluation | primary | primary | -- |
| 06.2 cnn evaluation | primary | -- | primary |
| 07.1 svm testing | primary | primary | -- |
| 07.2 cnn testing | primary | -- | primary |
| 08 comparison | primary | primary | primary |

**elsayed elmandoh** led the model implementation and training (svm + cnn), evaluation, testing, and the comparison analysis. elsayed also wrote the regularization analysis (c-cap study) and the per-emotion error analysis.

**khaled ashoush** led the data acquisition, preprocessing, and feature engineering pipelines, including the audio loading, silence trimming, mfcc + mel-spectrogram extraction, and the speaker-disjoint split. khaled also co-led the svm evaluation (notebook 06.1) and svm testing (07.1).

**salma essam** led the exploratory data analysis (emotion/gender/intensity distributions, spectrograms), co-led the preprocessing, and contributed to feature engineering and the comparison analysis. salma also co-led the svm training (notebook 05.1), cnn evaluation (06.2), and cnn testing (07.2).

**reports and presentation.** we contributed to drafting the midterm and final reports. elsayed and salma led the final report writing. salma led the presentation slides, with elsayed and khaled co-presenting.

**code reviews and pull requests.** we reviewed each other's pull requests and participated in design discussions throughout the project.
