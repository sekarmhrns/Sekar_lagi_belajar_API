from fastapi import FastAPI, HTTPException, Header 
import pandas as pd

app = FastAPI()
password = "seventeen17"

# endpoint 1 -> untuk membuka halaman utama
#setiap endpoint selalu ada function handlernya
@app.get('/') #selama ada / dianggap URL
def getLucky(): #function dalam api harus ada return nya
    return {
        "message": "Good Luck today!"
    }

'''untuk cek diterminal pake -> fastapi dev namafile'''

#endpoint 2 -> supaya bisa menampilkan data dari CSV
@app.get('/detail')
def getDetail():
    df = pd.read_csv('data.csv') #data drmanapun dibaca dulu dgn pandas
    #convert dataframe ke dictionary
    return {
        "message": "Tell me the details!",
        "data" : df.to_dict(orient="records") #orient untuk menentukan format penulisan yg diperlukan 
        #kalo gapake orient defaultnya dictionary biasa aja
    }

#endpoint 3 -> untuk menampilkan data specific pada csv
#path-parameter -> sebuah input yang bisa dimasukkan ke dalam URL
@app.get("/detail/{id}") #{parameter yg dipilih}
def getDatabyID(id: int):
    df = pd.read_csv('data.csv')
    #filter dgn method query
    resultID = df.query(f"id == {id}")

    #cek apakah hasil filter ada isinya
    # ada -> success, ga ada -> error
    if resultID.empty:
        # kasih hasil/respon error
        raise HTTPException(status_code=404, detail="data tidak ditemukan") #untuk ngasih return error

    return {
        "data": resultID.to_dict(orient="records")
    }

#endpoint 4 -> delete data by id
#apply authentication
@app.delete("/detail/{id}")
def deletedatabyID(id:int, api_key:str = Header()): #function handler + header untuk membuat header
    #check api_key
    # benar -> lanjut, salah -> error
    if api_key == None or api_key != password:
        #kasih error
        raise HTTPException(status_code=401, detail="password salah")
    df = pd.read_csv('data.csv')
    #filter dgn method query
    resultID = df.query(f"id == {id}")

    #cek apakah hasil filter ada isinya
    # ada -> success, ga ada -> error
    if df.empty:
        # kasih hasil/respon error
        raise HTTPException(status_code=404, detail="data tidak ditemukan") #untuk ngasih return error
    
    # delete -> exclude ID yg ada di parameter
    df = df.query(f"id != {id}")

    # update dataset -> replace dataset yang lama dgn yg baru
    df.to_csv('data.csv', index=False)

    return {
        "message": "data berhasil dihapus"
    }

#endpoint 4 -> tambah data
#@app.put()