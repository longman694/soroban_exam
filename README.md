# Soroban Exam

Get a soroban exam from www.sorobanexam.org.

You should only retrieve the exam once every 30 seconds.

## Install

```shell
pip install git+https://github.com/longman694/soroban_exam.git
```

## Useage

```bash
./soroban_exam.py -l 6 -m kojima
```

```bash
usage: soroban_exam [-h] [-l LEVEL] [-o OUTPUT] [-m {moritomo,kojima,cumin,namuec}]
                    [-s {Interactive,None,Inline,End,SplitEnd}]

options:
  -h, --help            show this help message and exit
  -l, --level LEVEL     level of exam (easiest 9 - hardest 1)
  -o, --output OUTPUT   output PDF name
  -m, --model {moritomo,kojima,cumin,namuec}
                        select exam model (default: moritomo)
  -s, --solution {Interactive,None,Inline,End,SplitEnd}
                        select exam solution (default: Inline)
```

## Install requirements

```
pip install -r requirements.txt
```
