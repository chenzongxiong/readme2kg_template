The vision of NFDI4DataScience (NFDI4DS) is to support all steps of the complex and interdisciplinary research data lifecycle, including collecting/creating, processing, analyzing, publishing, archiving, and reusing resources in Data Science and Artificial Intelligence. GitHub is a popular platform for hosting and collaborating on software projects. In the context of research, authors can use GitHub repositories to share the datasets, models, and source code of experiments in the paper. These repositories can provide implementation details and facilitate the exploration and reproduction of research results. Each GitHub repository typically includes a README.md file, which serves as an introductory document for the project. READMEs are usually written in Markdown format and provide key information such as the project’s purpose, setup instructions, usage examples, and often links to the original research paper. Aiming to enhance the NDFI4DS-KG[1] with information from GitHub README files, a fine-grained Named Entity Recognition task is proposed.

Participants will develop classifiers that take README files as input and output the mentions of the 10 entity types in the NFDI4DS Ontology (NFDI4DSO [2]): “Conference”, “Dataset”, “Evaluation Metric”, “License”, “Ontology”, “Programming Language”, “Project”, “Publication”, “Software” and ”Workshop”. A dataset with approximately 160 README.md files will be made available to train the classifiers.
* **Dataset**:  A dataset with approximately 160 README.md files will be made available to train the classifiers. Each file in the training set contains labeled sentence in WebAnno 3.3 format. 
* **Nested NER**: The annotation of a named entity can be nested in another named entity, for example, a publication title contains a software name. Thus a token can have different labels. Discontinuous named entities are not considered in this task.
* **Evaluation**: The NER systems will be evaluated based on the boundary detection of each entity type respectively. Only labeled sentences are evaluated. More specifications can be found in the Evaluation page.

Contact:
* Genet Asefa Gesese (genet-asefa.gesese@fiz-karlsruhe.de) 
* Zongxiong Chen (zongxiong.chen@fokus.fraunhofer.de)
* Shufan Jiang (shfuan.jiang@fiz-karlsruhe.de)

References:

[1] NFDI4DS-KG https://nfdi.fiz-karlsruhe.de/4ds/sparql, https://nfdi.fiz-karlsruhe.de/4ds/shmarql

[2] Genet Asefa Gesese et al. “NFDI4DSO: Towards a BFO Compliant Ontology for Data Science”. In: arXiv preprint arXiv:2408.08698 (2024).