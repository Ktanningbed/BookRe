import React, { useEffect } from 'react'
import { useState } from 'react'
import Novel from './Novel'


function Books() {

    const [books, setBooks] = useState([])

    useEffect(() => {
        // fetch("http://127.0.0.1:5000/api/novel").then((res) =>
        //     res.json().then((rows) =>{
        //         setBooks(rows)
        //     }))

        fetch("http://127.0.0.1:5000/api/novel").then((res) => 
            res.json()
            .then((data) => {
                setBooks(data)
            })
        )
    }, [])
        
    return (
        <div>
            
            {books.length>0?(
                
                <div className='flex'>{books.map((book) => 
                    <Novel author={book[1]} title={book[3]} img_url={book[4]}/>)}
                </div>
            ):(
                <div> no books</div>
            )}
        </div>
    )
}

export default Books