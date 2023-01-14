import React, { useState } from 'react'
import { useEffect } from 'react'
import Novel from './Novel'
import './style.css'

function Form() {

    const [author, setAuthor] = useState('')
    const [title, setTitle] = useState('')
    const [img, setImg] = useState('')
    const [books, setBooks] = useState([])
    const onSubmit = (e) => {
      e.preventDefault()
      fetch("http://127.0.0.1:5000/api/novel", {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({"author": author, "title": title, "image_url": img})}).then((res) => 
          res.json()
          .then((data) => {
            setBooks([data, ...books])
          })
      )
      
    }

    return (
      <div className='center'>
          <form onSubmit={onSubmit}>
              <div class="inputbox">
                  <input type="text" required="required" value={author} onChange={(e) => setAuthor(e.target.value)}/>
                  <span>Author</span>
              </div>
              <div class="inputbox">
                  <input type="text" required="required" value={title} onChange={(e) => setTitle(e.target.value)}/>
                  <span>Title</span>
              </div>
              <div class="inputbox">
                  <input type="text" required="required" value={img} onChange={(e) => setImg(e.target.value)}/>
                  <span>Image URL</span>
              </div>
              <button type='submit'></button>
          </form>

          <div>
              Newly added novels:
              {books.length>0?(
                
                <div className='flex'>{books.map((book) => 
                    <Novel author={book[0]} title={book[1]} img_url={book[2]}/>)}
                </div>
                ):(
                    <div></div>
                )}
          </div>
      </div>
    )
}

export default Form