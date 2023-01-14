import React from 'react'
import "./style.css"

function Novel({author, title, img_url}) {


        
    return (
        <div className='card'>
            <div className='heading'>
                
                <center className='text'>{title}</center> 
                <center className='text'>By {author}</center>
            </div>
            <img className='image' src={img_url} alt='novel image'/>
        </div>
  )
}

export default Novel