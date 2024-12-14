# 静态分析工具推荐系统

该项目旨在为给定的软件工程项目推荐最合适的静态分析工具。通过对多个静态分析工具（如 SpotBugs、SonarQube 和 PMD）进行扫描并结合项目特征，生成训练数据集，最终基于机器学习模型推荐最优的工具。

## 项目结构  
SAToolRecommendation  
├── dataset  
│   └── train_data  # 用于模型训练的数据集  
├── src  # 源代码文件夹  
│   ├── collect_datas  # 获取项目和版本信息的模块  
│   ├── data_process  # 数据处理和特征提取模块  
│   ├── get_findbugs_res  # 获取 SpotBugs 扫描结果  
│   ├── get_pmd_res  # 获取 PMD 扫描结果  
│   ├── get_revision  # 获取项目版本信息  
│   ├── get_sonarqube_res  # 获取 SonarQube 扫描结果  
│   ├── get_type_uniform  # 工具警告统一映射  
│   ├── model_training  # 模型训练及特征选择模块  
│   └── utils  # 实用工具类  
└── type_uniform  # 警告类型统一映射  
    ├── tables  # 各种静态分析工具警告类型的映射表  
    └── uniform  # 各工具警告类型的统一格式   


## 文件夹描述

### `dataset`
- 该文件夹包含用于模型训练的数据集。`train_data` 文件夹包含经过处理的项目特征数据集，这些数据将用于训练推荐模型。

### `src`
这是项目的主要源代码文件夹，包含不同功能模块的子文件夹：

- **collect_datas**: 该模块用于从 Git 仓库获取项目代码和版本信息。
- **data_process**: 负责数据的预处理和特征提取，将静态分析工具的扫描结果转化为结构化的项目特征。
- **get_checkstyle_res**, **get_findbugs_res**, **get_pmd_res**, **get_sonarqube_res**: 这些模块分别用于运行和收集各自静态分析工具（SpotBugs、PMD、SonarQube）的扫描结果。
- **get_revision**: 用于获取项目的版本信息以及相关的数据。
- **get_type_uniform**: 该模块负责将不同静态分析工具产生的警告统一映射为相同的类型，确保结果的一致性。
- **model_training**: 包含特征选择、数据准备以及模型训练脚本，最终用来推荐最合适的静态分析工具。
- **utils**: 提供各种实用的工具函数，如文件操作、Git 仓库操作等。

### `type_uniform`
- **tables**: 包含不同静态分析工具警告类型的映射表（如 SonarQube、FindBugs、PMD）。
- **uniform**: 存放统一格式的警告数据表，以确保不同工具的警告能够被一致地处理。

## 流程概述

1. **拉取项目仓库**  
   从 `repo_tag.list` 文件中列出的 Git 仓库中拉取项目，并获取指定版本的代码。

2. **执行静态分析工具**  
   使用 `SpotBugs`、`PMD`、`SonarQube` 等静态分析工具扫描项目，收集各工具的扫描报告。

3. **提取项目特征**  
   使用 `understand` 工具从项目中提取软件工程特征，并将这些特征处理为结构化数据。

4. **映射警告类型**  
   使用 `get_type_uniform` 模块将不同工具的警告映射为统一的类型，以便于后续处理和分析。

5. **生成训练数据集**  
   将处理后的项目特征与静态分析结果合并，生成训练模型所需的数据集，保存在 `dataset/train_data` 文件夹中。

6. **训练模型**  
   使用 `model_training` 模块中的脚本对数据进行特征选择和训练，最终得出推荐最合适静态分析工具的机器学习模型。
