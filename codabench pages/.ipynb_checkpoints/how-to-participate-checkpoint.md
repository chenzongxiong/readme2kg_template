1. Sign up on the [CodaBench competition platform](https://www.codabench.org/accounts/signup) 

2. Join the [ReadMe2KG competition](https://www.codabench.org/competitions/4925/)

3. To register for the task, go to **My Submissions**, accept the terms and conditions, and click **register**

4. Once registered, you can check the shared task’s files by:
Logging in to Codabench (**Login**) →  Clicking on **Benchmarks**→ Selecting **Management**

5. From the **Benchmark Management** page, click **Benchmarks I’m In**. Then, click on the shared task **ReadMe2KG**

6. **Download Data and Template Project** 
    * Template Project: [readme2kg_template](https://github.com/chenzongxiong/readme2kg_template)
    * Data are in [readme2kg_template/data](https://github.com/chenzongxiong/readme2kg_template/tree/main/data).

7. **Read Data** 
    * The training/validation/test data are all in WebAnno 3.3 TSV format.
    * Each .TSV file in the training folder is a Readme file with labeled sentences and unlabeled sentences.
    * The labeled sentences can be used for training and evaluating NER systems, while the unlabeled sentences can provide contextual information.
    * Each .TSV file in the unlabeled validation and test folder contains all the sentences of a Readme file. 
    * For evaluation, each label will only be evaluated with sentences that  are annotated with this label (see the **Evaluation** page for more details).
    * Code examples for parsing WebAnno .TSV are given in [readme2kg_template/src/predictor.py](https://github.com/chenzongxiong/readme2kg_template/blob/main/src/predictor.py). 

8. **Write Prediction Files**
    * One output file is expected for each README file.
    * Submit your prediction files in WebAnno TSV 3.3 format.
    * Ensure that the prediction files have the same names as the input files.
    * Predictions will be evaluated with the labeled (invisible to participants) sentences only; our scorer will ignore all non-overlapped predictions with the corresponding label's labeled sentences.
    * Code examples for writing WebAnno .TSV are given in [readme2kg_template/src/predictor.py](https://github.com/chenzongxiong/readme2kg_template/blob/main/src/predictor.py). 

9. **Submit Predictions**
	* a. Go to **My submissions**, select the **Phase** (Development or Evaluation Phase) to submit your predictions
	* b. **Submit as** allows you to submit as an individual or part of a group/organization you created.
	* c. Finally, select the zipped folder containing the predictions and upload it (scoring will automatically start).
	* d. Wait and check if the submission process is **Finished** or **Failed**.
    * e. Check the outputs and detailed results. 
    
10. **Development Phrase**
	* Develop your NER system with training data
	* Prepare your predictions for the validation data
    * Test your NER system with the [scorering script](https://github.com/chenzongxiong/readme2kg_template/blob/main/run_scoring.sh) on your local machine.
	* Submit your predictions to **Development Phrase**
 	* Teams can submit up to **999** submissions 

11. **Evaluation Phrase**
	* Pull the test data after **February 15, 2025**
	* Prepare your predictions for the test data
	* Submit your predictions to **Evaluation Phrase** 
 	* Teams can submit up to **3** submissions

12. **Leaderboard**
    * Once the submission is successful, the status will change to "Finished,” and your score can be added to the leaderboard. 
    * Note that the leaderboard will not be visible during the evaluation period (starting from **February 15, 2025**) and the official results will be published on **February 27, 2025**.