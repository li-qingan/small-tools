# 简介
这个python脚本文件，用于将一个sample.bib文件转换成sample-gb.bib文件。
- 输入文件：sample.bib，文件中包含多个bibtex格式的参考文献条目。
- 输出文件：sample-gb.txt，文件中包含对应输入文件的参考文献，但是格式是GB/T 7714。
- 命令: >python bibtex2gb.py sample.bib

# 使用场景
- 国内期刊投稿的参考文献格式
- 国内常用项目申请书参考文献格式
- 比如，dblp可以直接导出包含一个作者的所有文献条目的bibtex文件。

# 限制
- 目前仅支持article（期刊）、inproceedings（会议）格式。
