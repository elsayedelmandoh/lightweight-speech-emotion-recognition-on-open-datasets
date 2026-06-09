# midterm's feedback

Project: Lightweight Speech Emotion Recognition Using 1D CNNs         

Score: 77/100

Team: Elsayed Elmandoua, Khaled Ahmed, Salma Essam                   

Grader: Mohamed Ads

## CRITERION SCORES:
- Abstract (5):         1        
- Introduction (10):    10
- Related Work (10):    8         
- Dataset (5):          5
- Preprocessing (5):    5        
- Architecture (5):     5
- Baselines (5):        4        
- Metrics (5):          4
- Prelim. Results (20): 13        
- Timeline (10):        7
- Contributions (10):   10       
- GenAI (5):            5
- Writing/Refs (5):     2        
- Penalty:              0

## STRENGTHS:
1. Impeccable 4-stage sequential audio preprocessing suite, featuring clear, domain-justified resampling, silence gate trimming, and amplitude bounding steps.
2. High-quality diagnostic breakdowns tracking metric behavior across separate performance channels (speech vs. song) and acoustic intensity configurations.
3. Highly thorough and honest GenAI disclosure section detailing exact operational limits.

## MUST IMPROVE BEFORE FINAL REPORT:
1. The abstract suffers from a major factual contradiction that triggers a penalty. Section 1.4 claims preliminary metrics of 56.4% for the SVM baseline and 49.1% for the CNN. However, looking down at the actual empirical results tables in Section 5-E, the true calculated test accuracy for the preliminary SVM run is listed as 27.9%.   Correct the critical data contradiction between your abstract (claiming ~56%  accuracy) and your results table (showing 27.9%). Also, this is not how the abstract of a schintrif paper should be writter. refere to any paper to see how the abstrach is being writtern (one paragraph now as a list of paragraphs)

2. In the related work, only one paper from 2019–2026 . At least two additional recent SER papers are needed.

3. No second (simpler deep) baseline. a fine-tuned or shallow CNN would complete the required ≥2 baselines. 

4. No metric is mathematically defined with a formula.

5. in Preliminary Results, the 1D CNN has not been trained at all at midterm . The 49.1% figure in the abstract has no supporting table, training curve, or epoch-level detail in the results section; (2) no training curve figure is present anywhere. For a paper whose core contribution is the CNN, the absence of any CNN training result is a significant midterm gap. 

6. No specific dates within phases, and no student-assignment column in the timeline 

7. The team completely omitted a project GitHub repository link anywhere in the report, and it is required in the team contribution.

10. The reference list contains only 4 text-cited entries. This falls significantly short of the rubric's strict baseline requirement of >=8  professional references 