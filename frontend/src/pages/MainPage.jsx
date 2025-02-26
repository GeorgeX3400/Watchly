import { useState } from 'react'

import './../App.css'
import ContactPage  from './ContactPage';
import ProfilePage from './ProfilePage'; 
import WatchesPage from './WatchesPage';


function MainPage() {
  const [currentPage, setCurrentPage] = useState('watches')

  const handlePage = (e) => {
    setCurrentPage(e.target.value);
  }
  

  return <>
    <div id='topbar'>
      <div id='logo'>
        <h2>Watchly</h2>
      </div>
      <div id='pagesList'>
        <button value='watches' onClick={handlePage}>All Watches</button>
        <button value='profile' onClick={handlePage}>Profile</button>
        <button value='contact' onClick={handlePage}>Contact</button>
      </div>

      <div id='buttons'>
        <button>Log In</button>
        <button> Cart </button>
      </div>
    </div>
      {
        currentPage === 'watches' ? <WatchesPage></WatchesPage> : (currentPage === 'profile' ? <ProfilePage></ProfilePage> : <ContactPage></ContactPage>)
      }
  </>
  ;
}
export default MainPage
