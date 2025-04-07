# Static Code Analyzer Recommendation via Preference Mining

Static Code Analyzers (SCAs) have played a critical role in software quality assurance. However, SCAs with various static analysis techniques suffer from different levels of false positives and false negatives, thereby yielding varying effectiveness in SCAs. To detect more defects in a given project, it is a possible way to use more available SCAs for scanning this project. Due to producing unacceptable costs and overpowering warnings, invoking all available SCAs for the defect detection of a given project is impractical in real scenarios. To address the above problem, we are the first to propose a practical SCA recommendation approach via preference mining, which aims to select the most effective SCA for a given project. Specifically, our approach performs the SCA effectiveness evaluation to obtain the correspondingly optimal SCAs on projects under test. Subsequently, our approach performs the SCA preference mining via the project characteristics, thereby analyzing the intrinsic relation between projects under test and the correspondingly optimal SCAs. Finally, our approach constructs the SCA recommendation model based on projects under test and the associated characteristics. We conduct the experimental evaluation on three popular SCAs as well as 213 open-source and large-scale projects. The results present that our constructed SCA recommendation model outperforms four typical baselines by 2 ～ 11 times.

## Project Structure  
```
SAToolRecommendation  
├── Dataset_and_features  
│   ├── 100_features  # 100 representative feaures after the feature selection
│   ├── SCA effectiveness evaluation  #  warning reports and SCA evaluation results
│   ├── train_data  # training data, involving the training set with different beta and 314 features
│   ├── Projects in GHTorrent.list # 730 curated Java projects from GHTorrent
│   └── Project_detais # Characteristics information of 213 projects
├── Script  # source code file  
│   ├── collect_datas  # get projects with associated version info  
│   ├── data_process  # data processing and feature extraction   
│   ├── get_spotbugs_res  # get results from SpotBugs   
│   ├── get_pmd_res  # get results from PMD  
│   ├── get_revision  # get revision info  
│   ├── get_sonarqube_res  # get results from SonarQube
│   ├── get_type_uniform  # warning alignment  
│   ├── model_training  # feature selection and model training 
│   └── utils  # tool method, such as the file operation
└── Type_uniform  # the results of warning alignment
   
```

