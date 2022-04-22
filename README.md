# API for Computational Economics

## Abstract

This project provides HTTP interfaces for computing several commonly used analytical formulas in computational economics and data analysis, such as OLS or logit regression.

## How to use?
Our project use django, so you should install **python3** (Recommended version:3.6.8) and the following packages:

Numpy Scipy Pandas openpyxl xlrd xlwt Django plotnine matplotlib sklearn pandasql linearmodels

If you are in China, we suggest you install packages from Tsinghua University pypi mirrors.

```
python3 -m pip install numpy scipy pandas openpyxl xlrd xlwt Django plotnine pandasql linearmodels sklearn -i https://pypi.tuna.tsinghua.edu.cn/simple/
```
Now config your path to save files and image, open the file **zyp/configure.py**

```
{
    "file_path":"/opt/zypfile",
    "img_path":"/opt/zypimg",
    "api_domain":"http://127.0.0.1:8000/"
}
```

Now change the value of **file_path** and **img_path** to your custom settings(be sure you have the permission!), and set **api_domain** to your own domain.


After installing the required packages, you should enter the main directory of our project which is named after **zyp**, and execute following commands.
```
cd CE
python3 manage.py runserver 0.0.0.0:Port
#Port is a positive integer(we suggest you select a port more than 1024 when you debug it, 8000 is common)
```
Now our project is running on your computer!

## How to call?
At first, you should test whether you configure our project correctly.
```
curl 127.0.0.1:Port/version/

{"respCode": 0, "respData": {"api_name": "CE API", "version": "1.0.16"}, "errMsg": null}
```
If your consequence is consistent with given JSON string, congratulations!
## Enjoy it!
We provide a simple HTML page for our project, you can browse **http://127.0.0.1:Port** and enjoy it!
## API Documents
If you don't satisfy our preinstall page, you can change it according to existing API.

We provide intact API documents for public, with URL:

https://www.apifox.cn/apidoc/shared-b79d3f14-e20a-4a46-ab68-9e8beabcf077