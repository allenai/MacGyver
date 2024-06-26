## MacGyver: Are Large Language Models Creative Problem Solvers?
<p align="left">
  <a href='https://arxiv.org/abs/2311.09682'>
    <img src='https://img.shields.io/badge/Arxiv-2308.16905-A42C25?style=flat&logo=arXiv&logoColor=A42C25'>
  </a>
  <a href='https://arxiv.org/pdf/2311.09682.pdf'>
    <img src='https://img.shields.io/badge/Paper-PDF-yellow?style=flat&logo=arXiv&logoColor=yellow'>
  </a>
  <a href='https://github.com/allenai/MacGyver'>
    <img src='https://img.shields.io/badge/GitHub-Code-black?style=flat&logo=github&logoColor=white'></a>
</p>

MacGyver is a dataset consisting of over 1,600 **real-world verbal problems** deliberately designed to trigger **innovative usage of objects** and **necessitate out-of-the-box thinking**. Our dataset covers diverse topics, ranging from indoors/household, neutral, to outdoors. Some examples include:

![](https://github.com/allenai/MacGyver/blob/main/teaser_img.png?raw=true)

![](https://github.com/allenai/MacGyver/blob/main/teaser_img_2.png?raw=true)

Figure 1. Examples of the problems in our MacGyver
dataset with the GPT-4 and human answers. (Pictures, drawn by DALL·E 3, are solely
for illustration purposes and may not accurately reflect the text.)

***



### Data

#### [1. Macgyver Dataset] 

Our Macgyver Dataset can be downloaded in ```data/MacGyver```. In addtion to the problem setup and corresponding solution, each data point in ```problem_solution_pair.xlsx``` contains the solvability status, and whether solving the problem requires using tools unconventionally.

```additional_human_solutions.xlsx``` contains additional human solutions to our solvable subset.



 #### [2. Additional Annotationed Solutions]

In addition to the problem statements and correct solutions, we release **additional solution-annotation pairs**  (e.g.,  human annotations for all the machine/human solutions tested in benchmarking) in ```data/Benchmark_results```. We hope these additional 4,700 answer-annotation pairs, containing a full gradient of correctness (completely wrong, partially correct, correct but less efficient, and perfect), will facilitate future works in **automatic evaluation**.





### Code

We release the code to 

* the code to curate the dataset in ```code/progressive_data_creation```
* the prompt used to collect LLM solutions in ```code/collect_solutions```
* the prompt used in ```iterative self-reflect``` and ```convergent divergent thinking``` in ```code/progressive_data_creation```



Contact yufeit@g.ucla.edu if you have questions.


### Citation
If you find our paper/dataset/code helpful, please cite us using:

```bib
@inproceedings{tian2023macgyver,
  title = {MacGyver: Are Large Language Models Creative Problem Solvers?},
  author = {Tian, Yufei and Ravichander, Abhilasha and Qin, Lianhui and Bras, Ronan Le and Marjieh, Raja and Peng, Nanyun and Choi, Yejin and Griffiths, Thomas L. and Brahman, Faeze},
  year = {2024},
  booktitle = {Proceedings of NAACL},
  eprint = {2311.09682},
  url = {https://arxiv.org/abs/2311.09682},
  primaryclass = {cs.CL},
}
```
