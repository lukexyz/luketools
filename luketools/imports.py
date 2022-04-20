print("-== luketools/imports.py ==-")

import io,operator,sys,os,re,mimetypes,csv,itertools,json,shutil,glob,pickle,tarfile,collections
import hashlib,itertools,types,inspect,functools,random,time,math,bz2,typing,numbers,string
import multiprocessing,threading,urllib,tempfile,concurrent.futures,matplotlib,warnings,zipfile

from datetime import datetime
from pathlib import Path

# External modules
import matplotlib.pyplot as plt,numpy as np,pandas as pd,seaborn as sns
pd.options.display.max_columns = 500
pd.options.display.max_rows = 99
from IPython.display import display, Markdown

import altair as alt

from rich import print, pretty, traceback
# pretty.install()
# traceback.install()  # too verbose

# debugging
# from IPython.core.debugger import Tracer; Tracer()()

