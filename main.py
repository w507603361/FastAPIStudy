from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse


# 创建FastAPI应用实例
app = FastAPI()

class News(BaseModel):
    id: int
    title: str
    content: str

@app.get("/news/{id}", response_model=News)
async def get_news(id: int):
    if id < 1:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return { 
        "id": id,
        "title": f"新闻标题{id}",
        "content": f"新闻内容{id}"
    }
    



@app.get("/file", response_class=FileResponse)
async def get_file():
    return FileResponse("./files/1.png")

@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return "<h1>HTMLResponse测试</h1>"

class User(BaseModel):
    username: str = Field(default="张三", min_length=2, max_length=20, description="用户名长度在2到20之间")
    password: str = Field(..., min_length=2, max_length=100, description="密码长度在2到100之间")

@app.post("/register")
async def register_user(user: User):
    return {"message": f"用户 {user.username} 注册成功！"}

class Book(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="书籍标题长度在1到100之间")
    author: str = Field(default="黑马程序猿", min_length=1, max_length=50, description="作者姓名长度在1到50之间")
    price: float = Field(..., gt=0, description="书籍价格必须大于0")

@app.post("/books/")
async def create_book(book: Book):
    return {"message": f"书籍 {book.title} 创建成功！作者为：{book.author}，价格为：{book.price}"}



class Item(BaseModel):
    name: str           # 必填：商品名称
    description: str | None = None  # 可选：商品描述
    price: float        # 必填：商品价格
    tax: float | None = None        # 可选：税费

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

@app.get("/hello")
async def say_hello():
    return {"message": "Hello!"}

@app.get("/book/{book_id}")
async def get_book(book_id : int = Path(..., ge=1, le=100, description="书籍ID必须在1到100之间")):
    return {"book_id" : book_id, "title": f"这是第{book_id}本书"}
 
@app.get("/author/{name}")
async def get_name(name: str = Path(..., min_length=1, max_length=5, description="作者姓名长度在1到5之间")):
    return{"name": name, "name": f"普通用户{name}"}

@app.get("/news/news_list")
async def get_news_list(
    skip: int = Query(0, ge=0, le=100, description="跳过的新闻数量"),
    limit: int = Query(10, ge=1, le=100, description="获取的新闻数量")):
    return {"skip": skip, "limit": limit}


@app.post("/items/")
async def create_item(item: Item):
    # 创建新商品，接收JSON请求体。
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}