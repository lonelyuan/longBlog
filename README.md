# README

This project is a Flask website, using Flask-Migrate to manage the database. The front-end frame is Bootstrap, UI component from [Material Kit](https://www.creative-tim.com/product/material-kit) 

### Features:
- User system using Flask-Login, permission control using Flask-admin
- Database backend using SQLAlchemy
- Post articles supporting Markdown, renderer using Flask-PageDown(frontend) and markdown(backend)
- Upload pictures using Flask-Reuploaded (For bugs in Flask-uploads) 
- Unified comment model, Supporting multi-level reply
- Full Blueprint

### reference:

- [快速上手 - flask 中文文档](https://dormousehole.readthedocs.io/en/latest/quickstart.html) 
- [Flask-mega-tutorial](https://luhuisicnu.gitbook.io/the-flask-mega-tutorial-zh/)
- 《Flask Web开发：基于Python的Web应用开发实战》
- 文件上传系列：https://zhuanlan.zhihu.com/p/23731819?refer=flask

### run project

```
pip install -r requirements.txt
flask db init
flask run
```

### TODO
- Hot Bot using redis
- More elegant admin module
- api module for frontend separation