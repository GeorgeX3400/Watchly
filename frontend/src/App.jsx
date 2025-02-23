import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import ContactPage  from './pages/ContactPage';
import ProfilePage from './pages/ProfilePage'; 
import WatchesPage from './pages/WatchesPage';


function App() {
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
export default App
