# API for Computational Economics

## Abstract

This project provides HTTP interfaces for computing several commonly used analytical formulas in computational economics and data analysis, such as OLS or logit regression.

## How to use?
Our project use django, so you should install **python3** and the following packages:

Numpy Scipy Pandas openpyxl xlrd Django plotnine matplotlib

If you are in China, we suggest you install packages from Tsinghua University pypi mirrors.

```
python3 -m pip install numpy scipy pandas openpyxl xlrd Django plotnine -i https://pypi.tuna.tsinghua.edu.cn/simple/
```
Now config your path to save files and image, open the file **zyp/config.json**

```
{
    "file_path":"/opt/zypfile",
    "img_path":"/opt/zypimg",
    "api_domain":"http://127.0.0.1:8000/"
}
```

Now change the value of **file_path** and **img_path** to your custom settings(be sure you have the permission!)


After installing the required packages, you should enter the main directory of our project which is named after **zyp**, and execute following commands.
```
cd zyp
python3 manage.py runserver 0.0.0.0:8000
```
Now our project is running on your computer!

## How to call?
At first, you should test whether you configure our project correctly.
```
curl 127.0.0.1:Port

{"respCode": 0, "respData": {"api_name": "CE API", "version": "1.0.16"}, "errMsg": null}
```
If your consequence is consistent with given JSON string, congratulations!

## API Documents
We provide intact API documents for public, with URL:

https://www.apifox.cn/apidoc/shared-b79d3f14-e20a-4a46-ab68-9e8beabcf077